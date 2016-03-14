from uuid import UUID

from django.db.models import F

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Rating, Staff
from .serializers import RatingSerializer, StaffSerializer

class ListStaffAPIView(generics.ListAPIView):

    serializer_class = StaffSerializer

    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        return Staff.objects.all()

    def filter_queryset(self, queryset):
        filters = {'deleted_at': None}
        if self.request.GET.get('name', None):
            filters['name__icontains'] = self.request.GET.get('name')
        return queryset.filter(**filters)

    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data)


class RetrieveStaffAPIView(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def retrieve(self, request, pk):

        staff = self.get_object()
        serializer = self.serializer_class(staff, context={'request': request})

        data = serializer.data
        return Response(data)


class ListCreateRatingAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

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
        rating_data = data.get('rating')
        rating_data['user_id'] = request.user.id

        # Check if staff exists
        try:
            Staff.objects.get(pk=UUID(rating_data.get('staff_id')))
        except:
            return Response({'error': 'Staff member does not exist.'}, status.HTTP_400_BAD_REQUEST)

        if not rating_data['values'].get('overall', False):
            _sum = 0
            count = 0
            values = rating_data.get('values')
            for key in values:
                _sum += values[key]
                count += 1
            rating_data['values']['overall'] = _sum/count


        serializer = self.get_serializer(data=rating_data)

        if serializer.is_valid():
            rating = serializer.save()
            if serializer.is_valid(raise_exception=False):
                Staff.objects.filter(id=rating.staff_id).update(votes=F('votes')+1)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RetrieveRatingAPIView(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def retrieve(self, request, pk):

        rating = self.get_object()
        serializer = self.serializer_class(rating)

        data = serializer.data
        return Response(data)
