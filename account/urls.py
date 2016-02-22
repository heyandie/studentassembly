from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .api import (
    RegisterAPIView,
    ActivateAccountAPIView,
    ResendVerificationAPIView
    )


urlpatterns = [
    url(r'^api/register$', RegisterAPIView.as_view({'post':'create'}), name='register'),
    url(r'^verify_account/(?P<token>[0-9A-Za-z]+)$', ActivateAccountAPIView.as_view(), name='verify'),
    url(r'^api/token_auth$', obtain_jwt_token, name='auth'),
    url(r'^api/resend_verification$', ResendVerificationAPIView.as_view(), name='resend_verification'),
]

"""
Endpoints:

# api/register
params: {
    'email': 'email',
    'password': 'password'
}
returns User basic object

{
    "id": "f21dab09-38c2-4520-aa87-f480386b6bb6",
    "password": "bcrypt$$2b$12$nQ7pctM8SVlbjLRfPqtdn.6h19JV0qjSZuT39BjpX7XHokRjIfmAC",
    "last_login": null,
    "username": "4CFTW9",
    "email": "rabinoandie@gmail.com",
    "registered_at": "2016-02-16T12:35:20.110623Z",
    "is_verified": false,
    "verification_link": "http://localhost:8000/verify_account/RR4L7RLSW3E86DJ37TOQR189XT6KC9AV"
}

# verify/account/<verification_token>
returns
{
    "success": "Account has been verified"
}
or
{
    "error": "Invalid activation key"
}


# api/token-auth
params: {
    'email': 'email',
    'password': 'password'
}
returns
{
    'token':'token'
}


# api/resend_verification
params: {
    'email': 'email'
}
returns
{
    'error': 'Email address is not registered.'
}
or
{
    'error': 'Account has been already verified.'
}
or
{
    'success': 'An verification email has been sent.'
}

"""
