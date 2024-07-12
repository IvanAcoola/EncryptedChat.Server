from django.urls import re_path

from websocketapp.datatransfer import DataTransfer


websocket_urlpatterns = [
    re_path("ws/data/", DataTransfer.as_asgi()),

]