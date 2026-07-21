from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from courses.api.pagination import StandardPagination
from .serializers import SubjectSerializer, CourseSerializer
from courses.models import Subject, Course



class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled':True})


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))     # The base QuerySet to fetch objects
    serializer_class = SubjectSerializer    # Tells the ViewSet how to serializer the data before sending it as JSON.
    pagination_class = StandardPagination   # Controls how many results per page are returned.


# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))    # The base QuerySet to use to retrieve objects
#     serializer_class = SubjectSerializer    # The class to serializer objects
#     pagination_class = StandardPagination
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


# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer


# CUSTOM API VIEW FOR STUDENT ENROLLMENT IN THE COURSES
# class CourseEnrollView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post (self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled':True})
# THIS CLASS IS REPLACED BY ADDING THE actions() decorator to the  enroll() method in CourseViewSet




