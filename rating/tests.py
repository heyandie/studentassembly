from django.test import TestCase

from rest_framework import status
from rest_framework_jwt import utils
from rest_framework.test import APIClient, APITestCase

from account.models import User
from rating.models import Staff, Rating
from account.api import jwt_payload_handler


# Create your tests here.
class SubmitRatingTest(APITestCase):

    fixtures = ['user.json', 'staff.json', 'schools.json']

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

        staff = Staff.objects.get(pk=rating.staff_id)
        self.assertEqual(staff.votes, 1)


class StaffTest(APITestCase):

    fixtures = ['staff.json', 'schools.json']

    def testRetrieve(self):
        response = self.client.get('/api/staff/19c34cac-e378-43f0-bd78-9f72d7fc49dd')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testList(self):
        response = self.client.get('/api/staff')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testSearch(self):
        response = self.client.get('/api/staff?name=Juan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
