from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        read_only_fields = ('created_at', 'deleted_at')
        exclude = ('is_approved',)
