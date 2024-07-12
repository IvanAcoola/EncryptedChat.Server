# mysite/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EncryptedChatServer.settings")

import django

django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from EncryptedChatServer.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
