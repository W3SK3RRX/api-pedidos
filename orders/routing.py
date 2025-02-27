from django.urls import path
from orders.consumers import OrderStatusConsumer

websocket_urlpatterns = [
    path("ws/orders/<int:order_id>/", OrderStatusConsumer.as_asgi()),
]
