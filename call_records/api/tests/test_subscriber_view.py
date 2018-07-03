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
            "id": 1,
            "phone_number": 91981848675
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(json.loads(response.content), data)
