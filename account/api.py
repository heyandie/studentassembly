import json


from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateAccountSerializer

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        user = data['user']
        serializer = CreateAccountSerializer(data=user)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
