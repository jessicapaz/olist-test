from django.test import TestCase

from api.models import Subscriber
from api.models import CallStartRecord
from api.models import CallEndRecord
from api.models import Price
from api.models import BillRecord
from django.utils import timezone
import datetime
import decimal


class SubscriberTest(TestCase):
    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            first_name="Test",
            last_name="Test",
            phone_number=91981848675
        )

    def test_subscriber_fields(self):
        subscriber = Subscriber.objects.get(phone_number=91981848675)
        self.assertEqual(subscriber.phone_number, 91981848675)


class CallStartRecordTest(TestCase):
    def setUp(self):
        self.call_start_record = CallStartRecord.objects.create(
            id=1,
            timestamp='2016-02-29T12:00:00Z',
            call_id=3,
            source=99988526423,
            destination=9993468278
        )

    def test_call_start_record_fields(self):
        call_start_record = CallStartRecord.objects.get(call_id=3)
        self.assertEqual(call_start_record.id, 1)


class CallEndRecordTest(TestCase):
    def setUp(self):
        self.call_end_test = CallEndRecord.objects.create(
            id=1,
            timestamp='2016-02-29T12:00:00Z',
            call_id=3
        )
    
    def test_call_end_record_fields(self):
        call_end_record = CallEndRecord.objects.get(call_id=3)
        self.assertEqual(call_end_record.id, 1)


class PriceTest(TestCase):
    def setUp(self):
        self.price_test = Price.objects.create(
            tarrif_type='standard',
            standing_charge=0.36,
            call_charge=0.09
        )
    
    def test_price_fields(self):
        price_test = Price.objects.get(id=1)
        self.assertEqual(float(price_test.call_charge), 0.09)


class BillRecordTest(TestCase):
    def setUp(self):
        self.subscriber_create = Subscriber.objects.create(
            first_name="Test",
            last_name="Test",
            phone_number=91981848675
        )
        
        self.call_start_create = CallStartRecord.objects.create(
            id=1,
            timestamp='2016-02-29T12:00:00Z',
            call_id=3,
            source=99988526423,
            destination=9993468278
        )
        
        self.call_end_create = CallEndRecord.objects.create(
            id=1,
            timestamp='2016-02-29T13:35:00Z',
            call_id=3
        )

        self.subscriber = Subscriber.objects.get(first_name="Test")
        self.call_start = CallStartRecord.objects.get(call_id=3)
        self.call_end = CallEndRecord.objects.get(call_id=3)
        

        self.duration = self.call_end.timestamp - self.call_start.timestamp
        self.duration_format = (datetime.datetime.min + self.duration).time()

        self.start_hour = self.call_start.timestamp.hour

        if 6 <= self.start_hour < 22:
            self.price_test = Price.objects.create(
            tarrif_type='standard',
            standing_charge=0.36,
            call_charge=0.09
            ) 
        elif 22 >= self.start_hour < 6:
            self.price_test = Price.objects.create(
            tarrif_type='reduced',
            standing_charge=0.36,
            call_charge=0.00
            )
        
        self.price = Price.objects.get(id=1)
        self.minutes = self.duration.total_seconds()/60
        self.total_price =  float(self.price.call_charge)*float(self.minutes) + float(self.price.standing_charge)


        self.bill_record = BillRecord.objects.create(
            id=1,
            subscriber=self.subscriber,
            call_start_record=self.call_start,
            call_duration=self.duration_format,
            reference_month=self.call_end.timestamp.month,
            reference_year=self.call_end.timestamp.year,
            call_price=self.total_price
        )

    def test_bill_record_fields(self):
        bill_test = BillRecord.objects.get(id=1)
        self.assertEqual(float(bill_test.call_price), 8.91)
