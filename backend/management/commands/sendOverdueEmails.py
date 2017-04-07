from django.core.management.base import BaseCommand
from backend.models import Checkout, CheckoutItem, Item
from pinax.eventlog.models import log
from datetime import datetime
from templated_email import send_templated_mail

class Command(BaseCommand):
    help = 'Process to be called on a schedule for sending emails to students with overdue items'

    def handle(self, *args, **options):
        checkoutItems = CheckoutItem.objects.all()
        for ci in checkoutItems:
            if(ci.dateTimeDue < datetime.now and ci.dateTimeIn is None):
                print(ci.item)