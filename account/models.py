import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

def generate_username():
    while 1:
        from django.conf import settings
        import random, string

        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

        try:
            User.objects.get(username=username)
        except:
            return username

# Create your models here.
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, max_length=40, default=uuid.uuid4)
    username = models.CharField(max_length=127, unique=True, default=generate_username)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    registered_at = models.DateTimeField(auto_now_add=True, db_index=True)
    verified_email = models.BooleanField(default=False)
