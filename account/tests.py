from django.test import Client

from rest_framework import status
from rest_framework_jwt import utils
from rest_framework.test import APIClient, APITestCase

from account.models import User
from account.api import jwt_payload_handler


# Create your tests here.
class UserAPITest(APITestCase):

    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(email='rabinoandie@gmail.com')

    def testGetTokenAuth(self):
        pass
