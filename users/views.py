import pyotp
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from users.models import AccessLog
from users.api.serializers import AccessLogSerializer
from users.api.permissions import IsAdmin
from rest_framework.response import Response
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status


class TwoFactorLoginView(TokenObtainPairView):
    """Verifica senha e, se necessário, pede o código 2FA"""
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        otp = request.data.get("otp")  # Código OTP opcional

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_2fa_enabled:
            if not otp:
                user.generate_otp()
                return Response({"message": "Código OTP enviado para o e-mail."}, status=status.HTTP_206_PARTIAL_CONTENT)
            
            totp = pyotp.TOTP(user.otp_secret)
            if not totp.verify(otp):
                return Response({"error": "Código OTP inválido"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class AccessLogView(ListAPIView):
    """Lista os logs de acesso à API (apenas para admin)"""
    
    queryset = AccessLog.objects.all().order_by("-timestamp")
    serializer_class = AccessLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class Enable2FAView(APIView):
    """Ativa ou desativa a autenticação de dois fatores"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        enable = request.data.get("enable", False)

        user.is_2fa_enabled = enable
        if enable and not user.otp_secret:
            user.generate_otp()

        user.save()
        return Response({"message": f"2FA {'ativado' if enable else 'desativado'} com sucesso."})