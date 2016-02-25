from django.db import models
from django_pgjson.fields import JsonBField

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=32, unique=True, blank=False)
    category_type = models.IntegerField()
    questions = JsonBField(null=True)


class Report(models.Model):

    category = models.IntegerField(blank=False)
    text = models.TextField(blank=False)
    answers = JsonBField(null=True)
    user_id = models.UUIDField()
    files = JsonBField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    allow_publish = models.BooleanField(default=False)
