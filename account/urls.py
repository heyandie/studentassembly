from django.conf.urls import url


from .api import RegisterAPIView


urlpatterns = [
    url(r'^api/register$', RegisterAPIView.as_view(), name='register')
]
