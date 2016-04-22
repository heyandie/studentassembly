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

        ratings = Rating.objects.filter(staff_id=staff.id)
        if request.user.is_authenticated():
            try:
                user_rating = ratings.filter(user_id=request.user.id).all()[0]
                data['user_rating'] = RatingSerializer(user_rating).data
                ratings = ratings.exclude(user_id=request.user.id)
            except:
                data['user_rating'] = None

        ratings = RatingSerializer(ratings, many=True).data
        data['ratings'] = ratings
        return Response(data)


class ListCreateRatingAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.GET.get('user', None):
            return [IsAuthenticated()]

        return [IsAuthenticatedOrReadOnly()]

    def filter_queryset(self, queryset):
        filters = {'deleted_at': None}
        if self.request.GET.get('user', None):
            filters['user_id'] = self.request.GET.get('user')
        return queryset.filter(**filters)

    def list(self, request):

        if not self.request.GET.get('user', None) == str(request.user.id):
            return Response({}, status.HTTP_403_FORBIDDEN)

        queryset = self.queryset
        queryset = self.filter_queryset(queryset)
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

        rating_data['values']['overall'] = rating_data.get('overall_rating', 0)

        serializer = self.get_serializer(data=rating_data)

        if serializer.is_valid():
            rating = serializer.save()
            if serializer.is_valid(raise_exception=False):
                Staff.objects.filter(id=rating.staff_id).update(votes=F('votes')+1)
                Staff.objects.get(pk=rating.staff_id).update_rating()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RetrieveRatingAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def retrieve(self, request, pk):

        rating = self.get_object()
        serializer = self.serializer_class(rating)

        data = serializer.data
        return Response(data)

    def partial_update(self, request, *args, **kwargs):

        rating = self.get_object()
        if not rating.user_id == self.request.user.id:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)
        else:
            data = request.data
            serializer = self.get_serializer(rating, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy():
        pass
