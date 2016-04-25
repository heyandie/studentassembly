from django.conf.urls import url

from .api import (
    ListReportAPIView,
    CreateReportAPIView,
    RetrieveReportAPIView,
    ListCategoryAPIView,
    ListSchoolsAPIView,
    UpvoteReportAPIView,
    UnvoteReportAPIView,
)

urlpatterns = [
    url(r'^api/report/$', CreateReportAPIView.as_view(), name="create-report"),
    url(r'^api/report$', ListReportAPIView.as_view(), name="list-report"),
    url(r'^api/report/(?P<pk>[0-9]+)$', RetrieveReportAPIView.as_view({'get':'retrieve'}), name="retrieve-report"),
    url(r'^api/report/upvote$', UpvoteReportAPIView.as_view(), name="upvote-report"),
    url(r'^api/report/unvote$', UnvoteReportAPIView.as_view(), name="unvote-report"),
    url(r'^api/categories',ListCategoryAPIView.as_view({'get': 'list'}), name="list-categories"),
    url(r'^api/schools',ListSchoolsAPIView.as_view({'get': 'list'}), name="list-schools"),
]


"""
# api/report
Method: POST
Authorization Header {
    HTTP_AUTHORIZATION: JWT Token
}
Data: {
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
}
Returns
201 if created  or 400 if bad request


# api/report
Method: GET
Returns
List of reports with query parameters

    q = 'text query'
    category = 'category'
    school = 'school'
    limit = no. of reports to fetch
    user = user id of user, needs Authorization

Ex. /api/report?q=hate&category=discrimination&school=polytechnic
Ex. /api/report?user=2a0b5cc1530e4e2a9cd3bcd3c29de637 # Note: Needs Authorization
Ex. /api/report?limit=10

# api/report/<id>
Method: GET
Authorization: {
    HTTP_AUTHORIZATION: JWT Token
}
Returns
Report object or 404 if not found


# api/categories
Returns list of all categories with the questions associated with it

# api/schools
Returns list of all schools

"""
