from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Course

def subdomain_course_middleware(get_response):
    """
    Subdomain for courses
    """
    def middleware(request):
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # For example: "django.educaproject.com" → len=3, not www ✅ enters if block

            # get course for the given subdomain by taking the first part of the host_parts
            # and looks up the Course with that slug. Returns 404 if not found.
            course = get_object_or_404(Course, slug=host_parts[0])

            # for example -> "/courses/django/"
            course_url = reverse('course_detail', args=[course.slug])
            # redirect the current request to the course_detail view
            url = '{}://{}{}'.format(
                request.scheme,                 # "https"
                '.'.join(host_parts[1:]),      # "educaproject.com"
                course_url                      # "/courses/django/"
            )
            # -> "https://educaproject.com/courses/django/"
            return redirect(url)
        response = get_response(request)
        return response
    return middleware

