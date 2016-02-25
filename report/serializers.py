from rest_framework import serializers

from .models import Category, Report

class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report


class CategorySerializer(serializers.ModelSerializer):

    questions = serializers.ListField(child=JSONSerializerField(), allow_null=True)
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'category_type', 'questions'
        )
