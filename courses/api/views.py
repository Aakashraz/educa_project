from django.db.models import Count
from rest_framework import generics
from rest_framework import viewsets
from courses.api.pagination import StandardPagination
from .serializers import SubjectSerializer, CourseSerializer
from courses.models import Subject, Course



class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))    # The base QuerySet to use to retrieve objects
    serializer_class = SubjectSerializer    # The class to serializer objects
    pagination_class = StandardPagination
#   This pagination line will result in different JSON structure returned by the view, as the following structure:
# {
#     "count": 4,
#     "next": null,
#     "previous": null,
#     "results": [
#         {
#             "id": 1,
#             "title": "Mathematics",
#             ...
#         },
#         ...
#     ]
# }
# The following items are now part of the JSON returned:
# - count: The total number of results.
# - next: The URL to retrieve the next page. The value is 'null' when there are no following pages.
# - previous: The URL to retrieve the previous page. The value is 'null' when there are no previous pages.
# - results: A list with the serialized 'objects' returned on this page.


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer


