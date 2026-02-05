from rest_framework import generics
from serializers import SubjectSerializer
from courses.models import Subject



class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()    # The base QuerySet to use to retrieve objects
    serializer_class = SubjectSerializer    # The class to serializer objects


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


