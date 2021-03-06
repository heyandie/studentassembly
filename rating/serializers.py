from rest_framework import serializers

from account.models import User
from .models import Rating, Staff
from report.models import School

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        read_only_fields = ('created_at', 'deleted_at')
        exclude = ('is_approved',)

    def to_representation(self, instance):
        data = super(RatingSerializer, self).to_representation(instance)
        data['staff_name'] = Staff.objects.get(pk=data['staff_id']).name
        data['alias'] = User.objects.get(pk=data['user_id']).username
        school_id = Staff.objects.get(pk=data['staff_id']).school
        data['school'] = School.objects.get(pk=school_id).name
        del data['user_id']
        return data


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        read_only_fields = ('id', 'rating', 'created_at', 'deleted_at',)

    def to_representation(self, instance):
        data = super(StaffSerializer, self).to_representation(instance)
        data['school_id'] = School.objects.get(pk=data['school']).id
        data['school'] = School.objects.get(pk=data['school']).name
        return data
