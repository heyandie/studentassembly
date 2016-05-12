import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=32, unique=True, blank=False)
    category_type = models.IntegerField()
    questions = JSONField(null=True)


class School(models.Model):
    name = models.CharField(max_length=128, unique=True, blank=False)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, max_length=40, default=uuid.uuid4)
    category = models.IntegerField(null=False, db_index=True)
    text = models.TextField(blank=False)
    answers = JSONField(null=True)
    user_id = models.UUIDField()
    files = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True)
    allow_publish = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    school = models.IntegerField(blank=False, db_index=True)
    status = models.CharField(default="Pending", max_length=20)

class ReportVote(models.Model):

    user_id = models.UUIDField()
    report_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)


class ReportFollow(models.Model):

    user_id = models.UUIDField()
    report_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
