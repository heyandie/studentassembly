from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import User

class PasswordValidator(RegexValidator):
    regex = r'^[A-Za-z\d]{8,}$'
    message = "Password must be at least 8 characters containing only letters and numbers."

class CreateAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, validators=[PasswordValidator()])

    class Meta:
        model = User
        field = ('email', 'password')


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'].encode('utf-8'), salt=None, hasher='bcrypt')
        return User.objects.create(**validated_data)
