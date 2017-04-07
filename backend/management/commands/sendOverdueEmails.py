from django.core.management.base import BaseCommand
from backend.models import Checkout, CheckoutItem, Item
from pinax.eventlog.models import log
from datetime import datetime
from templated_email import send_templated_mail

class Command(BaseCommand):
    help = 'Process to be called on a schedule for sending emails to students with overdue items'

    def handle(self, *args, **options):
        overdue = CheckoutItem.objects.filter(dateTimeDue__lt=datetime.now(), dateTimeIn=None)
        for ci in overdue:
            nSent = send_templated_mail(
                template_name='itemOverdue',
                recipient_list=[ci.checkout.person.email],
                from_email=None,
                fail_silently=True,
                context={
                    'checkoutItem': ci
                }
            )
            if nSent == 0:
                log(
                    user='ScheduleTask',
                    action="EMAIL_SENDING_FAILED",
                    obj=None,
                    extra={
                        'email': 'itemOverdue',
                        'recipient_list': [ci.checkout.person.email]
                    }
                )
            else:
                log(
                    user='ScheduleTask',
                    action="EMAIL_SENT",
                    obj=None,
                    extra={
                        'email': 'itemOverdue',
                        'recipient_list': [ci.checkout.person.email]
                    }
                )