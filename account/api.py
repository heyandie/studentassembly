import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

from .models import User, VerificationToken
from .serializers import CreateAccountSerializer

def send_verification_request(recepient, link):
    from django.conf import settings
    from django.core.mail import EmailMessage

    template = get_template('email/verify_account.html')
    context = Context({'verification_link': link})
    content = template.render(context)
    subject = 'Please verfiy your email address'
    msg = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, [recepient])
    msg.content_subtype = "html"
    msg.send()


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountAPIView(APIView):

    permission_classes = (AllowAny,)
    def get(self, request, token):
        try:
            token = VerificationToken.objects.get(token=token)
            user = User.objects.get(id=token.user_id)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                token.delete()
                return Response({'success':'Account has been verified'}, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid activation key'})
