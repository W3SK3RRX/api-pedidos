import pyotp
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('funcionario', 'Funcionário'),
        ('admin', 'Administrador'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_2fa_enabled = models.BooleanField(default=False)  # 2FA ativado/desativado
    otp_secret = models.CharField(max_length=16, blank=True, null=True)  # Código secreto para gerar OTP

    def save(self, *args, **kwargs):
        """Garante que donos de restaurantes tenham um e-mail obrigatório"""
        if self.role == "funcionario" and not self.email:
            raise ValueError("Donos de restaurantes precisam de um e-mail para 2FA")
        super().save(*args, **kwargs)

    def generate_otp(self):
        """Gera um código OTP e envia por e-mail"""
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()
        
        otp = pyotp.TOTP(self.otp_secret).now()
        send_mail(
            "Seu código de autenticação",
            f"Seu código OTP é: {otp}",
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )
        return otp

    def __str__(self):
        return self.username


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} acessou {self.endpoint} ({self.method}) - {self.status_code}"
