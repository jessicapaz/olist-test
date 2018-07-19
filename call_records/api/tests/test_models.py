import datetime
import decimal
import pytz

from django.test import TestCase

from api.models import Subscriber
from api.models import CallStartRecord
from api.models import CallEndRecord
from api.models import Price
from api.models import BillRecord
from django.utils import timezone

from api.bill import Bill


class SubscriberTest(TestCase):
    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            first_name='Test',
            last_name='Test',
            phone_number='99988526423'
        )

    def test_subscriber_fields(self):
        subscriber = Subscriber.objects.get(phone_number='99988526423')
        self.assertEqual(subscriber.phone_number, '99988526423')


class CallStartRecordTest(TestCase):
    def setUp(self):
        self.subscriber_create = Subscriber.objects.create(
            first_name='Test',
            last_name='Test',
            phone_number='91981848675'
        )
        self.subscriber = Subscriber.objects.get(first_name='Test')
        self.call_start_record = CallStartRecord.objects.create(
            id=1,
            timestamp='2016-02-29T12:00:00Z',
            call_id=3,
            source=self.subscriber,
            destination="9993468278"
        )

    def test_call_start_record_fields(self):
        call_start_record = CallStartRecord.objects.get(call_id=3)
        self.assertEqual(call_start_record.id, 1)


class CallEndRecordTest(TestCase):
    def setUp(self):
        self.subscriber_create = Subscriber.objects.create(
            first_name='Test',
            last_name='Test',
            phone_number='99988526423'
        )
        self.subscriber = Subscriber.objects.get(first_name='Test')
        self.price_test_standard = Price.objects.create(
            tarrif_type='standard',
            standing_charge=0.36,
            call_charge=0.09
        )
        self.price_test_reduced = Price.objects.create(
            tarrif_type='reduced',
            standing_charge=0.36,
            call_charge=0.00
        )
        self.call_start_record = CallStartRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, tzinfo=pytz.UTC),
            call_id=3,
            source=self.subscriber,
            destination="9993468278"
        )
        self.call_end_test = CallEndRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2016, 2, 29, 13, 35, 0, tzinfo=pytz.UTC),
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
            phone_number="91981848675"
        )
        self.price_test_standard = Price.objects.create(
            tarrif_type='standard',
            standing_charge=0.36,
            call_charge=0.09
        )
        self.price_test_reduced = Price.objects.create(
            tarrif_type='reduced',
            standing_charge=0.36,
            call_charge=0.00
        )
        self.subscriber = Subscriber.objects.get(first_name="Test")
        self.call_start_create = CallStartRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2018, 2, 1, 12, 0, 45, tzinfo=pytz.UTC),
            call_id=3,
            source=self.subscriber,
            destination="9993468278"
        )
        self.call_end_create = CallEndRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2018, 2, 1, 13, 35, 35, tzinfo=pytz.UTC),
            call_id=3
        )
        self.call_start = CallStartRecord.objects.get(call_id=3)
        self.call_end = CallEndRecord.objects.get(call_id=3)
        self.duration = self.call_end.timestamp - self.call_start.timestamp
        self.duration_format = (datetime.datetime.min + self.duration).time()
        self.bill = Bill(self.call_start, self.call_end)
        self.call_price = self.bill.get_call_price()

        self.bill_record = BillRecord.objects.create(
            id=2,
            subscriber=self.subscriber,
            call_start_record=self.call_start,
            call_duration=self.duration_format,
            reference_month=self.call_end.timestamp.month,
            reference_year=self.call_end.timestamp.year,
            call_price=self.call_price
        )

    def test_bill_record_fields(self):
        bill_test = BillRecord.objects.get(id=2)
        self.assertEqual(float(bill_test.call_price), 8.91)
