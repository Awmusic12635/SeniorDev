from backend.models import Reservation, ReservationRequest, ItemType
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from backend.forms import ReservationRequestForm, ReservationRequestApprovalForm
from datetime import datetime
from templated_email import send_templated_mail
from pinax.eventlog.models import log

@login_required
def request(request):
    submitted = None
    if request.method == "POST":
        form = ReservationRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.requester = request.user
            obj.save()

            log(
                user=request.user,
                action="RESERVATION_REQUEST_SUBMITTED",
                obj=obj,
                extra={
                }
            )
            return redirect('reservationRequest')
    else:
            form = ReservationRequestForm()
    return render(request, 'reserveItem.html', {'title': 'Reserve Item', 'form': form, 'submitted': submitted})


@login_required
def view_requests(request):
    requests = ReservationRequest.objects.filter(approvedOn = None, approvedBy = None).filter(declinedOn = None, declinedBy = None).order_by('startDate')
    return render(request, 'reservationRequests.html', {'title': 'Pending Reservations', 'requests': requests})


@login_required()
def edit_request(request, request_id):
    if request.method == "POST":
        # get form data that may have been changed
        form = ReservationRequestApprovalForm(request.POST)
        if form.is_valid():
            # breakout item info if no specific type
            rr = ReservationRequest.objects.get(pk=request_id)
            if rr.itemTypeID is None:
                itemTypes = ItemType.objects.filter(subCategoryID=rr.itemSubCategoryID)
                for it in itemTypes:
                    # get an object
                    obj = form.save(commit=False)
                    obj.pk = None
                    obj.reservationRequestID = rr
                    obj.itemTypeID = it
                    obj.userID = rr.personRequestedFor
                    obj.save()
            else:
                # get an object
                obj = form.save(commit=False)
                obj.reservationRequestID = rr
                obj.itemTypeID = rr.itemTypeID
                obj.userID = rr.personRequestedFor
                obj.save()
            # set approval info
            rr.approvedBy = request.user
            rr.approvedOn = datetime.now()
            oldValues = rr.tracker.changed()
            # build the extras for the log
            rr.save()

            extras = {}
            for key in oldValues:
                extras.update({'old-' + key: oldValues[key]})
                extras.update({'new-' + key: rr.tracker.previous(key)})

            log(
                user=request.user,
                action="RESERVATION_REQUEST_APPROVED",
                obj=obj,
                extra=extras
            )
            # send email to notify of approval,nSent will be 1 if successful, 0 if failed
            # send email to notify of decline, nSent will be 1 if successful, 0 if failed
            nSent = send_templated_mail(
                template_name='reservationApproved',
                recipient_list=[rr.requester.email],
                from_email=None,
                fail_silently=True,
                context={
                    'request': rr,
                    'approvedInfo': form.save(commit=False)
                }
            )
            if nSent == 0:
                log(
                    user=request.user,
                    action="EMAIL_SENDING_FAILED",
                    obj=None,
                    extra={
                        'email' : 'reservationApproved',
                        'recipient_list' : [rr.requester.email]
                    }
                )
            else:
                log(
                    user=request.user,
                    action="EMAIL_SENT",
                    obj=None,
                    extra={
                        'email': 'reservationApproved',
                        'recipient_list' : [rr.requester.email]
                    }
                )

        return(view_requests(request))
    else:
        rr = get_object_or_404(ReservationRequest, pk=int(request_id))
        reservationInstance = Reservation
        reservationInstance.endDate = rr.endDate
        reservationInstance.startDate = rr.startDate
        reservationInstance.lengthOfCheckout = rr.lengthOfCheckout
        reservationInstance.quantity = rr.quantity
        form = ReservationRequestApprovalForm(instance=reservationInstance)
        return render(request, 'editReservation.html', {'title': 'Edit Reservation', 'request': rr, 'form':form})


@login_required()
def decline_request(request, request_id):
    if request.method == "POST":
        # get form data that may have been changed
        reason = request.POST['reason']
        rr = ReservationRequest.objects.get(pk=request_id)
        rr.declinedReason = reason
        rr.declinedBy = request.user
        rr.declinedOn = datetime.now()

        log(
            user=request.user,
            action="RESERVATION_REQUEST_DECLINED",
            obj=rr,
            extra={
            }
        )

        rr.save()

        #send email to notify of decline, nSent will be 1 if successful, 0 if failed
        nSent = send_templated_mail(
            template_name='reservationDecline',
            recipient_list=[rr.requester.email],
            from_email=None,
            fail_silently=True,
            context={
                'request': rr
            }
        )
        if nSent == 0:
            log(
                user=request.user,
                action="EMAIL_SENDING_FAILED",
                obj=None,
                extra={
                    'email' : 'reservationDecline',
                    'recipient_list' : [rr.requester.email]
                }
            )
        else:
            log(
                user=request.user,
                action="EMAIL_SENT",
                obj=None,
                extra={
                    'email': 'reservationDecline',
                    'recipient_list' : [rr.requester.email]
                }
            )
        return redirect('reservationRequestPending')


@login_required
def list_reservations(request):
    reservations = Reservation.objects.all().order_by('startDate')
    return render(request, 'viewReservations.html', {'title': 'View Reservations', 'reservations': reservations})
