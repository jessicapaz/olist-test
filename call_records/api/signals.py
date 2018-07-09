from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CallEndRecord
from .models import CallStartRecord
from .models import Subscriber
from .models import BillRecord

from .bill import Bill
import datetime


@receiver(post_save, sender=CallEndRecord)
def create_bill_record(sender, instance, created, **kwargs):
    if created:
        call_id = instance.call_id
        call_start = CallStartRecord.objects.get(call_id=call_id)
        subscriber = Subscriber.objects.get(
            phone_number=call_start.source.phone_number
        )
        duration = instance.timestamp - call_start.timestamp
        duration_format = (datetime.datetime.min + duration).time()
        bill = Bill(call_start)
        price = bill.calculate_price(duration)

        BillRecord.objects.create(
            subscriber=subscriber,
            call_start_record=call_start,
            call_duration=duration_format,
            reference_month=instance.timestamp.month,
            reference_year=instance.timestamp.year,
            call_price=price
        )
