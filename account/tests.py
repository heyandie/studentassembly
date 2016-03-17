from django.test import TestCase

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

    def testCreate(self):

        auth = 'JWT {0}'.format(self.token)
        response = self.client.get('/api/user', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.data['id'], str(self.user.id.hex))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
