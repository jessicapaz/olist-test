import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from api.models import Subscriber
from users.models import User


class SubscriberTestCase(APITestCase):
    url = '/subscriber/'

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "test"
        self.user = User.objects.create_user(self.email, self.password)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
    
    def test_create_subscriber(self):
        response = self.client.post(self.url, {"phone_number":"91981848675"})
        self.assertEqual(json.loads(response.content), {'id': 1, 'phone_number': '91981848675'})