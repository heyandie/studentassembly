from uuid import UUID

from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
import boto3

from account.models import User
from .models import Category, Report, School
from .serializers import CategorySerializer, ReportSerializer, SchoolSerializer

def _randomstr():
    while 1:
        from django.conf import settings
        import random, string

        string = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(20))

        return string


class ListReportAPIView(APIView):

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
            category = Category.objects.get(name__icontains=self.request.GET.get('q'))
            filters['category'] = category.id
            schools = School.objects.filter(name__icontains=self.request.GET.get('q')).only('id')
            filters['school__in'] = schools

        if self.request.GET.get('user', None):
            user_id = UUID(self.request.GET.get('user'))
            filters['user_id'] = user_id

        else:
            filters['allow_publish'] = True

        # TODO: Filter based on permission to publish report

        queryset = queryset.filter(**filters).order_by('-created_at')

        if self.request.GET.get('limit', None):
            limit = int(self.request.GET.get('limit'))
            return queryset[:limit]
        else:
            return queryset

    def get(self, request):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data)


class CreateReportAPIView(APIView):

    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def post(self, request, format=None):
        data = request.data
        report_data = data.get('report')
        report_data['user_id'] = request.user.id
        uploads = report_data['files']
        del report_data['files']

        contact = data.get('contact', {})
        user = User.objects.get(pk=request.user.id)

        name = contact.get('name', None)
        if name:
            user.name = contact.get('name', None)

        contact_number = contact.get('contact_number', None)
        if contact_number:
            user.contact_number = contact_number

        if name or contact_number:
            user.save()

        if uploads:
            from os.path import splitext
            from datetime import datetime
            report_data['files'] = {}
            random_string = _randomstr()

            botoclient = boto3.client('s3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            for i, f in enumerate(uploads):
                ext = splitext(f['name'])[1][1:].strip().lower()
                upload_timestamp = int(datetime.now().strftime("%s")) * 1000

                if not ('image' in f['type'] or 'pdf' in f['type']):
                    return Response({'error':'Invalid file type'}, status.HTTP_400_BAD_REQUEST)

                filename = 'uploads/{}_{}_{}.{}'.format(
                    random_string,
                    i,
                    upload_timestamp,
                    ext
                )
                r = botoclient.put_object(
                    ACL='public-read',
                    Body=f['blob'],
                    ContentType=f['type'],
                    Key=filename,
                    Bucket='studentassemblyph'
                )
                if r['ResponseMetadata']['HTTPStatusCode'] == 200:
                    url = 'http://{}/{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, filename)
                    report_data['files'][i] = url

        serializer = ReportSerializer(data=report_data)

        if serializer.is_valid():
            report = serializer.save()

            serializer.is_valid(raise_exception=True)

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

        if self.request.user.id == report.user_id or report.allow_publish:
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
