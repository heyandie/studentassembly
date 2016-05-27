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
        self.client = APIClient()
        self.user = User.objects.get(email='rabinoandie@gmail.com')
        payload = jwt_payload_handler(self.user)
        self.token = utils.jwt_encode_handler(payload)


    def testUpdateAccountDetails(self):
        auth = 'JWT {0}'.format(self.token)

        response = self.client.patch('/api/account/{}'.format(self.user.id),
            {
                "contact_number": '09175226502'
            }, HTTP_AUTHORIZATION=auth, format='json')

    def testChangePassword(self):
        auth = 'JWT {0}'.format(self.token)
        user = User.objects.get(email='rabinoandie@gmail.com')

        response = self.client.patch('/api/change_password'.format(self.user.id),
            {
                "password": 'corruptionsucks',
                "old_password": 'abcdefgh1'
            }, HTTP_AUTHORIZATION=auth, format='json')

        print(user.password)
        user = User.objects.get(email='rabinoandie@gmail.com')
        print(user.password)
