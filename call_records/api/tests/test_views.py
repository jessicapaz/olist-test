import json

from rest_framework.reverse import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from api.models import Subscriber
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

    def test_create_call_start_record(self):
        data = {
            'id': 1,
            'type': 'start',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70,
            'source': '99988526423',
            'destination': '9993468278'
        }
        response = self.client.post(self.url, data=data)
        data.pop('type')
        self.assertEqual(json.loads(response.content), data)

    def test_create_call_end_record(self):
        data = {
            'id': 1,
            'type': 'end',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70
        }
        response = self.client.post(self.url, data=data)
        data.pop('type')
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
