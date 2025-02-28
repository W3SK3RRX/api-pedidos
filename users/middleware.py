from users.models import AccessLog
from django.utils.timezone import now

class AccessLogMiddleware:
    """Middleware para registrar logs de acesso"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            AccessLog.objects.create(
                user=request.user,
                ip_address=request.META.get("REMOTE_ADDR"),
                endpoint=request.path,
                method=request.method,
                status_code=response.status_code,
                timestamp=now()
            )

        return response
