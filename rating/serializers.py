from rest_framework import serializers

from .models import Rating, Staff
from report.models import School

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        read_only_fields = ('created_at', 'deleted_at')
        exclude = ('is_approved',)


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        read_only_fields = ('id', 'rating', 'created_at', 'deleted_at',)

    def to_representation(self, instance):
        data = super(StaffSerializer, self).to_representation(instance)
        data['school'] = School.objects.get(pk=data['school']).name
        data['overall_rating'] = data['rating'].get('overall', 0)
        del data['rating']['overall']
        return data
