from django.core.management.base import BaseCommand
from backend.models import CheckoutItem, User
from pinax.eventlog.models import log
from datetime import datetime
from templated_email import send_templated_mail

class Command(BaseCommand):
    help = 'Process to be called on a schedule for sending an email to the admin with a list of overdue items'

    def handle(self, *args, **options):
        overdue = CheckoutItem.objects.filter(dateTimeDue__lt=datetime.now(), dateTimeIn=None)
        admins = User.objects.filter(is_superuser=1)
        print(admins)
        emails = []
        for a in admins:
            emails.append(a.email)
        print(emails)
        nSent = send_templated_mail(
            template_name='itemOverdueSummary',
            recipient_list=emails,
            from_email=None,
            fail_silently=True,
            context={
                'checkoutItems': overdue
            }
        )
        if nSent == 0:
            log(
                user=None,
                action="EMAIL_SENDING_FAILED",
                obj=None,
                extra={
                    'email': 'itemOverdueSummary',
                    'recipient_list': emails
                }
            )
        else:
            log(
                user=None,
                action="EMAIL_SENT",
                obj=None,
                extra={
                    'email': 'itemOverdueSummary',
                    'recipient_list': emails
                }
            )