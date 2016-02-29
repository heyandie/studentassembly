from rest_framework import serializers

from .models import Category, Report, School


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'category_type', 'questions'
        )
