from django.test import TestCase

from api.models import Subscriber
from api.models import CallStartRecord
from api.models import CallEndRecord
from api.models import Price


class SubscriberTest(TestCase):
    def setUp(self):
        self.subscriber = Subscriber.objects.create(
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
            tarrif_type='reduced',
            standing_charge=0.36,
            call_charge=0.09
        )
    
    def test_price_fields(self):
        price_test = Price.objects.get(id=1)
        self.assertEqual(price_test.id, 1)