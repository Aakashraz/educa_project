from django.urls import include, path
from rest_framework import routers
from . import views


app_name = 'courses'

router = routers.DefaultRouter()    # Creating a DefaultRouter object.
router.register('courses', views.CourseViewSet)     # This registers CourseViewSet with the 'courses' prefix.
# **`router.register('courses', views.CourseViewSet)`** does two things:
# 1. Takes the **prefix** `'courses'` — this becomes the URL segment
# 2. Inspects the **ViewSet class** — checks what actions are available (`list`, `retrieve`, etc.)
# Then internally it builds a URL pattern map like:
# ```
# prefix = 'courses'
# viewset = CourseViewSet → has list() and retrieve() (ReadOnlyModelViewSet)
#
# Generated patterns:
#   'courses/'      → list action
#   'courses/{pk}/' → retrieve action
#
# Then include(router.urls) --
# path('', include(router.urls)),
# ```
#
# `router.urls` is just a **list of URL patterns** that the router built during `register()`. Using `path('', ...)` mounts them at the root of this file's URL namespace.
#
# Since this `urls.py` is in the `courses` app and likely included in the main `urls.py` under `api/`, the full path becomes:
# ```
# /api/courses/       → list
# /api/courses/{pk}/  → retrieve
# ```
router.register('subjects', views.SubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),

]