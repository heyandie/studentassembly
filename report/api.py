from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .models import Category, Report
from .serializers import CategorySerializer, ReportSerializer

class ListCreateReportAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]

        return [IsAuthenticatedOrReadOnly()]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data)

    def create(self, request, format=None):
        data = request.data
        serializer = ReportSerializer(data=data)

        if serializer.is_valid():
            report = serializer.save()
            data['id'] = report.id
            return Response(data, status=status.HTTP_201_CREATED)
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
