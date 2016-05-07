from rest_framework import serializers

from account.models import User
from .models import Category, Report, School, ReportVote


class ReportFullSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    class Meta:
        model = Report

    def to_representation(self, instance):
        data = super(ReportFullSerializer, self).to_representation(instance)
        data['school_id'] = data['school']
        data['school'] = School.objects.get(pk=data['school']).name
        category = Category.objects.get(pk=data['category'])
        data['questions'] = category.questions
        data['category'] = category.name
        data['alias'] = User.objects.get(pk=data['user_id']).username
        data['upvotes'] = ReportVote.objects.filter(report_id=data['id']).count()
        del data['user_id']
        return data


class ReportBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        exclude = ('answers', 'files',)

    def to_representation(self, instance):
        data = super(ReportBasicSerializer, self).to_representation(instance)
        data['school_id'] = data['school']
        data['school'] = School.objects.get(pk=data['school']).name
        category = Category.objects.get(pk=data['category'])
        data['category'] = category.name
        data['alias'] = User.objects.get(pk=data['user_id']).username
        del data['user_id']
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
