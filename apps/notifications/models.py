from django.db import models
from apps.core.models import BaseModel


class Notification(BaseModel):
    TYPE_CHOICES = (
        ('order_confirmed', 'Buyurtma tasdiqlandi'),
        ('order_shipped', 'Buyurtma yetkazilmoqda'),
        ('order_delivered', 'Buyurtma yetkazildi'),
        ('order_cancelled', 'Buyurtma bekor qilindi'),
        ('payment_received', "To'lov qabul qilindi"),
        ('promo', 'Aksiya'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    title = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)

    message = models.TextField()
    message_uz = models.TextField(null=True, blank=True)
    message_ru = models.TextField(null=True, blank=True)

    data = models.JSONField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)


class DeviceToken(BaseModel):
    PLATFORM_CHOICES = (
        ('android', 'Android'),
        ('ios', 'iOS'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=500)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    is_active = models.BooleanField(default=True)