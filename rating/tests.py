from django.test import TestCase

from rest_framework import status
from rest_framework_jwt import utils
from rest_framework.test import APIClient, APITestCase

from account.models import User
from rating.models import Staff, Rating
from account.api import jwt_payload_handler


# Create your tests here.
class SubmitRatingTest(APITestCase):

    fixtures = ['user.json', 'staff.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(email='rabinoandie@gmail.com')
        payload = jwt_payload_handler(self.user)
        self.token = utils.jwt_encode_handler(payload)

    def testCreate(self):

        auth = 'JWT {0}'.format(self.token)
        staff = Staff.objects.latest('id')
        response = self.client.post('/api/rating/', {
            'rating': {
                'staff_id': staff.id,
                'values': {
                    'attendance': 3,
                    'communication_skills': 4,
                    'accessibility': 4,
                    'efficiency': 5,
                    'fairness': 3
                }
            }

        }, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating = Rating.objects.latest('id')
        response = self.client.get('/api/rating/'+str(rating.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
