from django.test import TestCase

from rest_framework import status
from rest_framework_jwt import utils
from rest_framework.test import APIClient, APITestCase

from account.models import User
from account.api import jwt_payload_handler
# Create your tests here.

class CreateReportTest(APITestCase):

    fixtures = ['categories.json', 'user.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(email='rabinoandie@gmail.com')
        payload = jwt_payload_handler(self.user)
        self.token = utils.jwt_encode_handler(payload)

    def testCreateRetrieveReport(self):


        auth = 'JWT {0}'.format(self.token)

        response = self.client.post('/api/report/', {
            'report': {
                'user_id': self.user.id,
                'category': 1,
                'text': 'I really hate you.'
            },
            'contact': {
                'name': 'Andie Rabino',
                'contact_number': '09175226502'
            }

        }, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.user = User.objects.get(email='rabinoandie@gmail.com')
        self.assertEqual(self.user.name, 'Andie Rabino')
        self.assertEqual(self.user.contact_number, '09175226502')

        response = self.client.get('/api/report/1', HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/report', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def testUnauthorizedCreateReport(self):
        response = self.client.post('/api/report/', {
            'user_id': self.user.id,
            'category': 1,
            'text': 'I really hate you.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
