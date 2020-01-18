from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from bgapp import routing

application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})