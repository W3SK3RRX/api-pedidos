from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/users/', include('users.api.urls')),
    path('api/restaurants/', include('restaurants.api.urls')),  # 🔹 Certifique-se de que está correto
    path('api/orders/', include('orders.api.urls')),
]
