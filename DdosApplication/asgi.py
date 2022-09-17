"""
ASGI config for DdosApplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import DdosTool.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DdosApplication.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            DdosTool.routing.websocket_urlpatterns
        )
    ),
})
