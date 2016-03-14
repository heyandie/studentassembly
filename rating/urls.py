from django.conf.urls import url

from .api import (
    RetrieveRatingAPIView,
    ListCreateRatingAPIView
)

urlpatterns = [
    url(r'^api/rating/(?P<pk>[0-9]+)', RetrieveRatingAPIView.as_view({'get':'retrieve'}), name="retrieve-rating"),
    url(r'^api/rating', ListCreateRatingAPIView.as_view(), name="create-rating"),
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

"""
