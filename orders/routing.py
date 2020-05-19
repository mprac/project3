from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'2/1', consumers.SectionConsumer)
]