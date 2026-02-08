from django.db.models import Count
from rest_framework import generics
from courses.api.pagination import StandardPagination
from .serializers import SubjectSerializer
from courses.models import Subject



class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))    # The base QuerySet to use to retrieve objects
    serializer_class = SubjectSerializer    # The class to serializer objects
    pagination_class = StandardPagination


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer


