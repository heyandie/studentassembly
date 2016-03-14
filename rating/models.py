import uuid


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import JSONField


# Create your models here.
class Staff(models.Model):
    id = models.UUIDField(primary_key=True, max_length=40, default=uuid.uuid4)
    name = models.CharField(max_length=128)
    school = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    rating = JSONField(default={
                'attendance': 0,
                'communication_skills': 0,
                'accessibility': 0,
                'efficiency': 0,
                'fairness': 0,
                'overall': 0
            })
    votes = models.IntegerField(default=0)

    def update_rating(self):
        ratings = Rating.objects.get(pk=self.id)
        count = 0
        _sum = {
            'attendance': 0,
            'communication_skills': 0,
            'accessibility': 0,
            'efficiency': 0,
            'fairness': 0,
            'overall': 0
        }
        for item in ratings:
            for key in item:
                _sum[key] += item[key]
                count += 1

        self.rating = {key: _sum[key]/count for key in _sum}
        self.save()
        

class Rating(models.Model):
    staff_id = models.UUIDField(max_length=40, default=uuid.uuid4)
    user_id = models.UUIDField(max_length=40, default=uuid.uuid4)
    values = JSONField(null=False)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ['staff_id', 'user_id']
