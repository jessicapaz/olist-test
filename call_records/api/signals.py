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
        call_start = get_object_or_404(CallStartRecord, call_id=call_id)
        subscriber = get_object_or_404(
            Subscriber,
            phone_number=call_start.source.phone_number
        )
        duration = instance.timestamp - call_start.timestamp
        duration_seconds = duration.total_seconds()
        duration_format = (datetime.datetime.min + duration).time()
        bill = Bill(call_start, instance)
        try:
            price = bill.get_call_price()
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
            call_duration=duration_format,
            reference_month=instance.timestamp.month,
            reference_year=instance.timestamp.year,
            call_price=price
        )
