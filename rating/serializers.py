from rest_framework import serializers

from .models import Rating, Staff


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        read_only_fields = ('created_at', 'deleted_at')
        exclude = ('is_approved',)


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        read_only_fields = ('id', 'rating', 'created_at', 'deleted_at',)
