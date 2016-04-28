from django.test import TestCase

from rest_framework import status
from rest_framework_jwt import utils
from rest_framework.test import APIClient, APITestCase

from account.models import User
from account.api import jwt_payload_handler
from report.models import Report
# Create your tests here.

class CreateReportTest(APITestCase):

    fixtures = ['categories.json', 'user.json', 'schools.json']

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
                'text': 'I really hate you.',
                'school': 1,
                'allow_publish': 'True'
            },
            'contact': {
                'name': 'Andie Rabino',
                'contact_number': '09175226502'
            }

        }, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        report = Report.objects.latest('created_at')
        self.assertEqual(True, report.allow_publish)

        self.user = User.objects.get(email='rabinoandie@gmail.com')
        self.assertEqual(self.user.name, 'Andie Rabino')
        self.assertEqual(self.user.contact_number, '09175226502')

        response = self.client.get('/api/report/'+str(report.id), HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/report', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/report?user='+str(self.user.id.hex), HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/report?limit=1', format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/report?q=Discrimination', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test first upvote = success
        response = self.client.post('/api/report/upvote', {
            'report_id': report.id,
            'user_id': self.user.id
        }, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/report/'+str(report.id), HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.data['vote'], True)

        response = self.client.get('/api/report?user='+str(self.user.id.hex)+'&upvoted=True', HTTP_AUTHORIZATION=auth, format='json')
        print(response.data)


    def testUnauthorizedCreateReport(self):
        response = self.client.post('/api/report/', {
            'user_id': self.user.id,
            'category': 1,
            'text': 'I really hate you.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
