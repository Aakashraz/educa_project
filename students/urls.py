from django.urls import path
from . import views
from django.views.decorators.cache import cache_page    # for caching



urlpatterns = [
    path(
        'register/', views.StudentRegistrationView.as_view(), name='student_registration'
    ),
    path(
        'enroll_course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'
    ),
    path(
        'courses/', views.StudentCourseListView.as_view(), name='student_course_list'
    ),
    # Different URL = Different cache entry, even if the same view processes it.
    # Each different URL gets its own separate cache, even if they use the same view.
    path(
        'course/<pk>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail'
    ),
    path(
        'course/<pk>/<module_id>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'
    ),
]