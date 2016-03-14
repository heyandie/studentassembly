from rest_framework import serializers

from .models import Category, Report, School


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report

    def to_representation(self, instance):
        data = super(ReportSerializer, self).to_representation(instance)
        data['school'] = School.objects.get(pk=data['school']).name
        return data


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'category_type', 'questions'
        )
