from django.conf.urls import url

from .api import (
    ListCreateReportAPIView,
    RetrieveReportAPIView,
    ListCategoryAPIView
)

urlpatterns = [
    url(r'^api/report/(?P<pk>[0-9]+)', RetrieveReportAPIView.as_view({'get':'retrieve'}), name="retrieve-report"),
    url(r'^api/report', ListCreateReportAPIView.as_view(), name="create-report"),
    url(r'^api/categories',ListCategoryAPIView.as_view({'get': 'list'}), name="list-categories"),
]


"""
# api/report
Method: POST
Authorization Header {
    HTTP_AUTHORIZATION: JWT Token
}
Data: {
    'category': integer,
    'text': 'text',
    'files': 'files',
    'allow_publish': boolean
}
Returns
201 if created  or 400 if bad request


# api/report
Method: GET
Returns
List of reports

# api/report/<id>
Method: GET
Authorization: {
    HTTP_AUTHORIZATION: JWT Token
}
Returns
Report object or 404 if not found


# api/categories
Returns list of all categories with the questions associated with it

"""
