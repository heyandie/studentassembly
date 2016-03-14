from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from account.models import User
from .models import Category, Report, School
from .serializers import CategorySerializer, ReportSerializer, SchoolSerializer

class ListCreateReportAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]

        return [IsAuthenticatedOrReadOnly()]

    def filter_queryset(self, queryset):
        filters = {'deleted_at': None}
        if self.request.GET.get('q', None):
            filters['text__icontains'] = self.request.GET.get('q')
        if self.request.GET.get('category', None):
            category = Category.objects.get(name=self.request.GET.get('category'))
            filters['category'] = category.id
        if self.request.GET.get('school', None):
            schools = School.objects.filter(name__icontains=self.request.GET.get('school')).only('id')
            filters['pk__in'] = schools

        # TODO: Filter based on permission to publish report

        return queryset.filter(**filters)

    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data)

    def create(self, request, format=None):
        data = request.data
        report_data = data.get('report')
        report_data['user_id'] = request.user.id

        contact = data.get('contact', {})
        user = User.objects.get(pk=request.user.id)
        user.name = contact.get('name', None)
        user.contact_number = contact.get('contact_number', None)
        user.save()

        serializer = ReportSerializer(data=report_data)

        if serializer.is_valid():
            report = serializer.save()
            serializer.is_valid(raise_exception=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RetrieveReportAPIView(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def retrieve(self, request, pk):

        report = self.get_object()
        serializer = self.serializer_class(report)

        if self.request.user.id == report.user_id:
            data = serializer.data

            return Response(data)
        else:
            return Response({}, status.HTTP_403_FORBIDDEN)


class ListCategoryAPIView(mixins.ListModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        serializer = self.serializer_class(data=self.queryset, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data)


class ListSchoolsAPIView(mixins.ListModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def list(self, request):
        serializer = self.serializer_class(data=self.queryset, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data)
