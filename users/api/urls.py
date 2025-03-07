from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from users.api.viewsets import RegisterView, UserViewSet
from users.views import AccessLogView, Enable2FAView, TwoFactorLoginView, LogoutView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logs/", AccessLogView.as_view(), name="access-log"),

    path("enable-2fa/", Enable2FAView.as_view(), name="enable-2fa"),
    path("login/", TwoFactorLoginView.as_view(), name="login-2fa"),
    path('', include(router.urls)),  # 🔹 Incluímos o router
]
