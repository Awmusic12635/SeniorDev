from django.core.management.base import BaseCommand
from backend.models import Checkout, CheckoutItem, Item
from pinax.eventlog.models import log
from datetime import datetime
from templated_email import send_templated_mail

class Command(BaseCommand):
    help = 'Process to be called on a schedule for sending emails to students with overdue items'

    def handle(self, *args, **options):
        overdue = CheckoutItem.objects.filter(dateTimeDue__lt datetime.now(), dateTimeIn is None)
        for ci in overdue:
            print(ci)