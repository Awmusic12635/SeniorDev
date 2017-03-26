from backend.models import Reservation, ReservationRequest
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from backend.forms import ReservationRequestForm


@login_required
def request(request):
    if request.method == "POST":
        form = ReservationRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.requester = request.user
            obj.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('reservationRequest')
    else:
        form = ReservationRequestForm()
        return render(request, 'requestReservation.html', {'title': 'Reserve Item', 'form': form})
