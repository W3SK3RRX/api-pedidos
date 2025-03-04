from django.urls import re_path
from restaurants.consumers import RestaurantRequestConsumer

websocket_urlpatterns = [
    re_path(r"ws/admin/notifications/$", RestaurantRequestConsumer.as_asgi()),
]
