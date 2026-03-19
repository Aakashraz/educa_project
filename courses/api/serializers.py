from django.db.models import Count
from rest_framework import serializers
from courses.models import Subject, Course, Module



class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    # This method is called by using the name convention as: get_(field_name of SerializerMethodField())
    # And the field must be included inside the fields of Meta class.
    def get_popular_courses(self,obj):
        # The 'obj' parameter is the model instance currently being serialized. In this case 'subject_instance'
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('total_students')[:3]
        return [
            f'{c.title} ({c.total_students})' for c in courses
        ]

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']



class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    # This 'modules' field that provides serialization for the related Module objects
    # many=True - indicate that you are serializing multiple related objects.
    # read_only=True - indicates that the field is read-only and should not be included in any
    #                  input to create or update objects.
    class Meta:
        model = Course
        fields = [ 'id', 'subject', 'title', 'slug', 'overview', 'created',
                   'owner', 'modules'
                ]


