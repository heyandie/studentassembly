from uuid import UUID
from functools import reduce
import operator

from django.db.models import F, Q

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Rating, Staff
from report.models import School
from .serializers import RatingSerializer, StaffSerializer

class ListStaffAPIView(generics.ListAPIView):

    serializer_class = StaffSerializer

    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        return Staff.objects.all()

    def filter_queryset(self, queryset):
        kwargs = {'deleted_at': None}
        args = ()
        if self.request.GET.get('q', None):
            search_query = self.request.GET.get('q').split()

            def _get_schools(q):
                return School.objects.filter(name__icontains=self.request.GET.get('q')).only('id')

            args = reduce(operator.or_, ((Q(name__icontains=x)|Q(school__in=_get_schools(x))) for x in search_query))
            args = (args,)
        # TODO: Filter based on permission to publish report

        queryset = queryset.filter(*args, **kwargs)

        if self.request.GET.get('user', None):
            user_id = UUID(self.request.GET.get('user'))
            queryset = queryset.filter(user_id=user_id)

        if self.request.GET.get('school', None):
            school = self.request.GET.get('school')
            queryset = queryset.filter(school=school)

        queryset = queryset.order_by('-created_at')

        if self.request.GET.get('limit', None):
            limit = int(self.request.GET.get('limit'))
            return queryset[:limit]
        else:
            return queryset

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
        user_id = UUID(self.request.GET.get('user', None))

        if not str(user_id) == str(request.user.id):
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

    def update(self, request, *args, **kwargs):

        rating = self.get_object()
        if not rating.user_id == self.request.user.id:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)
        else:
            data = request.data['rating']
            serializer = self.get_serializer(rating, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            Staff.objects.get(pk=rating.staff_id).update_rating()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy():
        pass
