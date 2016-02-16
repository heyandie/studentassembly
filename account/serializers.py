from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import User

class PasswordValidator(RegexValidator):
    regex = r'^(?=.*\d)[A-Za-z\d]{8,}$'
    message = "Passwords must be minimum of 8 characters and only contain letters or numbers with at least 1 number."

class CreateAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, validators=[PasswordValidator()])

    class Meta:
        model = User
        field = ('email', 'password')


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'].encode('utf-8'), salt=None, hasher='bcrypt')
        return User.objects.create(**validated_data)
