"""
ASGI config for vistaHardware project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/

"""
"""Dev Notes (Lani): In general, ASGI defines how a Python web server communicates with web applications."""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import camera.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vistaBackend.settings')

application = ProtocolTypeRouter({
        "http": get_asgi_application(), #Ensures that Django can handle normal traffic (ex: manager)
        "websocket": AuthMiddlewareStack( #Handles WebSocket connections like real-time communication
            URLRouter(
                camera.routing.websocket_urlpatterns
            )
        ),
})
