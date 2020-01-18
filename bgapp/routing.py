from django.urls import re_path
from . import consumers
from . import test_consumers

websocket_urlpatterns = [
    #re_path(r'wss/chat/$', test_consumers.TestConsumer),
    re_path(r'wss/chat/$', consumers.ChatConsumer),
]