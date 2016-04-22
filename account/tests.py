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

        print (response.content)
