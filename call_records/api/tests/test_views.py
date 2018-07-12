import json
import datetime
import pytz
import decimal

from rest_framework.reverse import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from api.models import Subscriber
from api.models import CallStartRecord
from api.models import BillRecord
from api.models import CallEndRecord
from api.models import Price

from users.models import User


class SubscriberTestCase(APITestCase):
    url = reverse('v1:subscriber-create')

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "test"
        self.user = User.objects.create_user(self.email, self.password)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_subscriber(self):
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "91981848675"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(json.loads(response.content), data)


class CallRecordTestCase(APITestCase):
    url = reverse('v1:call-record')

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "test"
        self.user = User.objects.create_user(self.email, self.password)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.subscriber = Subscriber.objects.create(
            first_name='Test',
            last_name='Test',
            phone_number='99988526423'
        )
        self.price_test_standard = Price.objects.create(
            tarrif_type='standard',
            standing_charge=0.36,
            call_charge=0.09
        )

    def test_create_call_start_record(self):
        subscriber = Subscriber.objects.get(first_name='Test')
        data = {
            'id': 1,
            'type': 'start',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70,
            'source': subscriber.phone_number,
            'destination': '9993468277'
        }
        response = self.client.post(self.url, data=data)
        data.pop('type')
        self.assertEqual(json.loads(response.content), data)

    def test_create_call_end_record(self):
        subscriber = Subscriber.objects.get(first_name='Test')
        data = {
            'id': 1,
            'type': 'start',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70,
            'source': subscriber.phone_number,
            'destination': '9993468277'
        }
        response = self.client.post(self.url, data=data)
        data = {
            'id': 1,
            'type': 'end',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70
        }
        response = self.client.post(self.url, data=data)
        data.pop('type')
        self.assertEqual(json.loads(response.content), data)

    def test_get_call_records(self):
        subscriber = Subscriber.objects.get(first_name='Test')
        call_start = {
            'id': 1,
            'type': 'start',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70,
            'source': subscriber.phone_number,
            'destination': '9993468277'
        }
        response = self.client.post(self.url, data=call_start)
        call_end = {
            'id': 1,
            'type': 'end',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70
        }
        response = self.client.post(self.url, data=call_end)
        data = {
            'call_start_records': [
                {
                    'id': 1,
                    'timestamp': '2016-02-29T12:00:00Z',
                    'call_id': 70,
                    'source': 99988526423,
                    'destination': '9993468277'
                }
            ],
            'call_end_records': [
                {
                    'id': 1,
                    'timestamp': '2016-02-29T12:00:00Z',
                    'call_id': 70
                }
            ]
        }
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), data)


class PriceTestCase(APITestCase):
    url = reverse('v1:price-create')

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "test"
        self.user = User.objects.create_user(self.email, self.password)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_price(self):
        data = {
            "id": 1,
            "tarrif_type": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(json.loads(response.content), data)


class BillRecordTestCase(APITestCase):
    url = reverse('v1:call-record')

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "test"
        self.user = User.objects.create_user(self.email, self.password)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.subscriber = Subscriber.objects.create(
            first_name='Test',
            last_name='Test',
            phone_number='99988526423'
        )
        self.subscriber = Subscriber.objects.get(first_name="Test")
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
        self.call_start_create = CallStartRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, tzinfo=pytz.UTC),
            call_id=3,
            source=self.subscriber,
            destination="9993468278"
        )
        self.call_end_create = CallEndRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2016, 2, 29, 13, 35, 0, tzinfo=pytz.UTC),
            call_id=3
        )

    def test_get_bill_record(self):
        subscriber = Subscriber.objects.get(first_name="Test")
        data = {
            "id": 1,
            "subscriber_id": 99988526423,
            "call_start_record_id": 1,
            "call_duration": datetime.time(1, 35),
            "reference_month": 2,
            "reference_year": 2016,
            "call_price": decimal.Decimal("8.91"),
        }
        bill = BillRecord.objects.filter(subscriber=subscriber).values().last()
        self.assertEqual(bill, data)
