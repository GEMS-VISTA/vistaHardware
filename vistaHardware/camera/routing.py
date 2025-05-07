"""
Routing.py sets up the WebSocket URL patterns (basically urls.py for WebSockets instead of HTTP)
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/video_feed/$', consumers.VideoFeedConsumer.as_asgi()),
]