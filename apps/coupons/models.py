from django.db import models
from apps.core.models import BaseModel


class Coupon(BaseModel):
    TYPE_CHOICES = (
        ('percentage', 'Foiz'),
        ('fixed', 'Belgilangan summa'),
        ('free_delivery', 'Bepul yetkazish'),
    )

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    usage_limit = models.IntegerField(null=True, blank=True)
    per_user_limit = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class CouponUsage(BaseModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2)