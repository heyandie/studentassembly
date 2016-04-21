from rest_framework import serializers

from .models import Category, Report, School


class ReportFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report

    def to_representation(self, instance):
        data = super(ReportFullSerializer, self).to_representation(instance)
        data['school'] = School.objects.get(pk=data['school']).name
        category = Category.objects.get(pk=data['category'])
        data['questions'] = category.questions
        data['category'] = category.name
        return data


class ReportBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ('answers',)

    def to_representation(self, instance):
        data = super(ReportBasicSerializer, self).to_representation(instance)
        data['school'] = School.objects.get(pk=data['school']).name
        category = Category.objects.get(pk=data['category'])
        data['category'] = category.name
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
