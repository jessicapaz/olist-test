import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from users.models import User


class CallEndRecordTestCase(APITestCase):
    url = '/call_record/'

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "test"
        self.user = User.objects.create_user(self.email, self.password)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
    
    def test_create_call_end_record(self):
        data = {
            'id':1,
            'type': 'end',
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(json.loads(response.content), {
            'id':1,
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': 70
        })