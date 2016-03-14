from django.conf.urls import url

from .api import (
    RetrieveRatingAPIView,
    ListCreateRatingAPIView,
    RetrieveStaffAPIView,
    ListStaffAPIView,
)

urlpatterns = [
    url(r'^api/rating/(?P<pk>[0-9]+)', RetrieveRatingAPIView.as_view({'get':'retrieve'}), name="retrieve-rating"),
    url(r'^api/rating', ListCreateRatingAPIView.as_view(), name="create-rating"),
    url(r'^api/staff/(?P<pk>[A-Za-z0-9\-]+)', RetrieveStaffAPIView.as_view({'get':'retrieve'}), name="retrieve-staff"),
    url(r'^api/staff', ListStaffAPIView.as_view(), name="list-staff"),
]


"""
# api/rating
Method: POST
Authorization Header {
    HTTP_AUTHORIZATION: JWT Token
}
Data: {
    'user_id': self.user.id,
    'staff_id': staff.id,
    'values': {
        'attendance': 3,
        'communication_skills': 4,
        'accessibility': 4,
        'efficiency': 4,
        'fairness': 3
    }
}
Returns
201 if created  or 400 if bad request

# api/staff
Method: GET
Optional Params:
    name: name of staff
Example: 'api/staff?name=Juan'
Returns
List of all staff matching query if there is

#api/staff/<staff_id>
Method: GET
Returns:
Staff object
Example: 'api/staff/19c34cac-e378-43f0-bd78-9f72d7fc49dd'
"""
