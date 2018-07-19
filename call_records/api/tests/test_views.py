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

from api.views import Subscriber

class SubscriberTestCase(APITestCase):
    url = reverse('v1:subscriber-list')
    url_detail = reverse('v1:subscriber-detail', kwargs={'pk':91981848675})

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
    
    def test_list_subscriber(self):
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "91981848675"
        }
        response = self.client.post(self.url, data=data)
        data_expected = [
                {
                    "first_name": "Test",
                    "last_name": "Test",
                    "phone_number": "91981848675"
                }
        ]
        response = self.client.get(self.url)
        self.assertEqual(json.loads(response.content), data_expected)
    
    def test_retrieve_subscriber(self):
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "91981848675"
        }
        response = self.client.post(self.url, data=data)
        data_expected = {
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "91981848675"
        }
        response = self.client.get(self.url_detail)
        self.assertEqual(json.loads(response.content), data_expected)

    def test_delete_subscriber(self):
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "91981848675"
        }
        response = self.client.post(self.url, data=data)
        response_delete = self.client.delete(self.url_detail, data=data)
        self.assertEqual(response_delete.status_code, 204)

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
                    'source':  '99988526423',
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
    url = reverse('v1:price-list')
    url_detail = reverse('v1:price-detail', kwargs={'pk':1})

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
    
    def test_list_price(self):
        data = {
            "id": 1,
            "tarrif_type": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09"
        }
        response = self.client.post(self.url, data=data)
        data_expected = [
            {
                "id": 1,
                "tarrif_type": "standard",
                "standing_charge": "0.36",
                "call_charge": "0.09"
            }
        ]  
        response = self.client.get(self.url)
        self.assertEqual(json.loads(response.content), data_expected) 
    def test_retrieve_price(self):
        data = {
            "id": 1,
            "tarrif_type": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09"
        }
        response = self.client.post(self.url, data=data)
        data_expected = {
            "id": 1,
            "tarrif_type": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09"
        }
        response = self.client.get(self.url_detail)
        self.assertEqual(json.loads(response.content), data_expected)

    def test_delete_price(self):
        data = {
            "id": 1,
            "tarrif_type": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09"
        }
        response = self.client.post(self.url, data=data)
        response_delete = self.client.delete(self.url_detail, data=data)
        self.assertEqual(response_delete.status_code, 204)

class BillRecordTestCase(APITestCase):
    url = reverse('v1:bill-record', kwargs={
        'phone_number':99988526423
    })

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
            timestamp=datetime.datetime(2018, 4, 30, 20, 8, 45, tzinfo=pytz.UTC),
            call_id=3,
            source=self.subscriber,
            destination="99988526423"
        )
        self.call_end_create = CallEndRecord.objects.create(
            id=1,
            timestamp=datetime.datetime(2018, 5, 1, 22, 5, 35, tzinfo=pytz.UTC),
            call_id=3
        )

    def test_get_bill_record(self):
        data_expected = {
            'bill_records': [
                {
                    'call_duration': '25:56:50',
                    'call_price': '96.84',
                    'call_start_date': '2018-04-30',
                    'call_start_time': '20:08:45',
                    'destination': '99988526423'
                }
            ],
            'subscriber': 'Test Test',
            'total_price': 96.84
        }
            
        response = self.client.get(f'{self.url}?month=5&year=2018')
        self.assertEqual(json.loads(response.content), data_expected)
