from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import CallEndRecord
from .models import CallStartRecord
from .models import Subscriber
from .models import BillRecord

from .bill import Bill
import datetime
from decimal import Decimal
from rest_framework.exceptions import NotFound

@receiver(post_save, sender=CallEndRecord)
def create_bill_record(sender, instance, created, **kwargs):
    if created:
        call_id = instance.call_id
        try:
            call_start = CallStartRecord.objects.get(call_id=call_id)
        except:
            instance.delete()
            error_message = """
            Call start is required,
            create a call start before create a call end.
            """
            raise NotFound(detail=error_message)

        subscriber = get_object_or_404(
            Subscriber,
            phone_number=call_start.source.phone_number
        )
        bill = Bill(call_start, instance)
        try:
            price = bill.get_call_price()
            duration = bill.get_call_duration()
        except:
            instance.delete()
            error_message = """
            Price (standard and reduced) is required, 
            create a price before create a call
            """
            raise NotFound(detail=error_message)
        BillRecord.objects.create(
            subscriber=subscriber,
            call_start_record=call_start,
            call_duration=duration,
            reference_month=instance.timestamp.month,
            reference_year=instance.timestamp.year,
            call_price=price
        )
