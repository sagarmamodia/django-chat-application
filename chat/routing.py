from django.urls import re_path

from . import consumers

websocket_patterns = [
    re_path(r"ws/chat/(?P<other_user>\w+)/$", consumers.ChatConsumer.as_asgi()),
]