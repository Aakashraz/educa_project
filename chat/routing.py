from django.urls import re_path
from . import consumers



websocket_urlpatterns = [
    re_path(
        r'ws/chat/room/(?P<course_id>\d+)/$',
        consumers.ChatConsumer.as_asgi()
    ),

]

# ?P	tells regex "this is a named group" (Python-specific syntax)
# <course_id>	the name you're giving to whatever is captured
# \d+	the actual pattern being captured.
# For example, 43 is captured and stored under the name course_id. Without ?P<course_id>
# it would still match 43, but you couldn't access it by name in your consumer -- you'd have
# to use positional indexing, which is messy