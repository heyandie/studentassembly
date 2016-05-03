import json
import jwt
import warnings
from calendar import timegm
from datetime import datetime


from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.utils.translation import ugettext as _

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions

from .models import User, VerificationToken
from .serializers import AccountSerializer, CreateAccountSerializer

def send_verification_request(recepient, link):
    from django.conf import settings
    from django.core.mail import EmailMessage

    template = get_template('email/verify_account.html')
    content = template.render({'verification_link': link})
    subject = 'Please verfiy your email address'
    msg = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, [recepient])
    msg.content_subtype = "html"
    msg.send()


def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )
    if not user.is_verified:
        msg = _('Please verify your account.')
        raise exceptions.AuthenticationFailed(msg)

    payload = {
        'user_id': str(user.id.hex),
        'alias': user.username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token, 'alias': user.username
    }


class RegisterAPIView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    query = User.objects.all()
    serializer_class = CreateAccountSerializer

    def create(self, request, format=None):
        user = request.data
        serializer = CreateAccountSerializer(data=user)

        if serializer.is_valid():
            user = serializer.save()
            token = VerificationToken.objects.create(user_id=user.id)
            data = serializer.data
            data['verification_link'] = request.build_absolute_uri(reverse('account:verify', kwargs={'token':token.token}))

            send_verification_request(data.get('email'), data.get('verification_link'))
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserContactDetailsAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.GET.get('contact', None) == 'true':
            data = {
                'name': request.user.name,
                'email': request.user.email,
                'contact_number': request.user.contact_number
            }
        else:
            data = {
                'id': str(request.user.id.hex),
                'username': request.user.username,
                'name': request.user.name,
                'email': request.user.email,
                'contact_number': request.user.contact_number
            }
        return Response(data)


class UpdateUserDetailsAPIView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.id == request.user.id:
            return Response({}, status.HTTP_403_FORBIDDEN)
        else:
            data = request.data
            serializer = self.get_serializer(user, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            return Response({}, status=status.HTTP_200_OK)


class ResendVerificationAPIView(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Email address is not registered'}, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            return Response({'error': 'Account has been already verified'}, status.HTTP_400_BAD_REQUEST)

        token = VerificationToken.objects.get(user_id=user.id)
        verification_link = request.build_absolute_uri(reverse('account:verify', kwargs={'token':token.token}))
        send_verification_request(email, verification_link)
        return Response({},status.HTTP_200_OK)
