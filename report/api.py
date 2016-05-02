from uuid import UUID
from functools import reduce
import operator

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
import boto3

from account.models import User
from .models import Category, Report, School, ReportVote, ReportFollow
from .serializers import CategorySerializer, ReportFullSerializer, ReportBasicSerializer, SchoolSerializer

def _randomstr():
    while 1:
        from django.conf import settings
        import random, string

        string = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(20))

        return string

class UpvoteReportAPIView(APIView):

    queryset = Report.objects.all()
    def get_permissions(self):
        return [IsAuthenticated()]

    def post(self, request):
        data = request.data
        vote, created = ReportVote.objects.get_or_create(user_id=data['user_id'], report_id=data['report_id'])
        if created:
            return Response({}, status.HTTP_200_OK)
        else:
            return Response({'error': 'Upvote for this report already exists'}, status.HTTP_400_BAD_REQUEST)


class UnvoteReportAPIView(APIView):

    queryset = Report.objects.all()
    def get_permissions(self):
        return [IsAuthenticated()]

    def post(self, request):
        data = request.data
        try:
            ReportVote.objects.get(user_id=data['user_id'], report_id=data['report_id']).delete()
            return Response({}, status.HTTP_200_OK)
        except:
            return Response({'error': 'No previous upvote record exists'}, status.HTTP_400_BAD_REQUEST)


class FollowReportAPIView(APIView):

    queryset = Report.objects.all()
    def get_permissions(self):
        return [IsAuthenticated()]

    def post(self, request):
        data = request.data
        vote, created = ReportFollow.objects.get_or_create(user_id=data['user_id'], report_id=data['report_id'])
        if created:
            return Response({}, status.HTTP_200_OK)
        else:
            return Response({'error': 'User already follows this report'}, status.HTTP_400_BAD_REQUEST)


class UnfollowReportAPIView(APIView):

    queryset = Report.objects.all()
    def get_permissions(self):
        return [IsAuthenticated()]

    def post(self, request):
        data = request.data
        try:
            ReportFollow.objects.get(user_id=data['user_id'], report_id=data['report_id']).delete()
            return Response({}, status.HTTP_200_OK)
        except:
            return Response({'error': 'No previous upvote record exists'}, status.HTTP_400_BAD_REQUEST)


class ListReportAPIView(APIView):

    queryset = Report.objects.all()
    serializer_class = ReportBasicSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def filter_queryset(self, queryset):
        kwargs = {'deleted_at': None}
        args = ()
        if self.request.GET.get('q', None):
            search_query = self.request.GET.get('q').split()

            def _get_categories(q):
                return Category.objects.filter(name__icontains=self.request.GET.get('q')).only('id')

            def _get_schools(q):
                return School.objects.filter(name__icontains=self.request.GET.get('q')).only('id')

            args = reduce(operator.or_, ((Q(text__icontains=x)|Q(category__in=_get_categories(x))|Q(school__in=_get_schools(x))) for x in search_query))
            args = (args,)

        # TODO: Filter based on permission to publish report

        queryset = queryset.filter(*args, **kwargs)

        if self.request.GET.get('user', None):
            user_id = UUID(self.request.GET.get('user'))
            queryset = queryset.filter(user_id=user_id)

        else:
            queryset = queryset.filter(allow_publish=True)

        if self.request.GET.get('school', None):
            school = self.request.GET.get('school')
            queryset = queryset.filter(school=school)

        queryset = queryset.order_by('-created_at')

        if self.request.GET.get('limit', None):
            limit = int(self.request.GET.get('limit'))
            return queryset[:limit]
        else:
            return queryset

    def get(self, request):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        data = {}
        data['reports'] = serializer.data

        if self.request.GET.get('user', None) and self.request.GET.get('upvoted', False):
            upvoted = [x.report_id for x in ReportVote.objects.filter(user_id=UUID(self.request.GET.get('user'))).all()]
            upvoted_reports = self.queryset.filter(id__in=upvoted)
            serializer = self.serializer_class(upvoted_reports, many=True)
            data['upvoted'] = serializer.data

            following = [x.report_id for x in ReportFollow.objects.filter(user_id=UUID(self.request.GET.get('user'))).all()]
            following_reports = self.queryset.filter(id__in=following)
            serializer = self.serializer_class(following_reports, many=True)
            data['following'] = serializer.data


        return Response(data)


class CreateReportAPIView(APIView):

    queryset = Report.objects.all()
    serializer_class = ReportFullSerializer

    def post(self, request, format=None):
        data = request.data
        report_data = data.get('report')
        report_data['user_id'] = request.user.id
        uploads = report_data.get('files', None)

        if 'files' in report_data:
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

        serializer = ReportFullSerializer(data=report_data)

        if serializer.is_valid():
            report = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RetrieveReportAPIView(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Report.objects.all()
    serializer_class = ReportFullSerializer

    def retrieve(self, request, pk):

        report = self.get_object()
        serializer = self.serializer_class(report)

        if self.request.user.is_anonymous() and not report.allow_publish:
            return Response({}, status.HTTP_403_FORBIDDEN)

        if self.request.user.id == report.user_id or report.allow_publish:
            data = serializer.data

            if self.request.user.is_authenticated():
                vote = ReportVote.objects.filter(report_id=report.id, user_id= self.request.user.id).all()
                if len(vote) > 0:
                    data['vote'] = True
                else:
                    data['vote'] = False

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
