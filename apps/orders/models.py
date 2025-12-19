from django.db import models
from apps.core.models import BaseModel


class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('preparing', 'Tayyorlanmoqda'),
        ('shipping', 'Yetkazilmoqda'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', "To'langan"),
        ('failed', 'Muvaffaqiyatsiz'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Naqd'),
        ('payme', 'Payme'),
        ('click', 'Click'),
        ('card', 'Karta orqali'),
    )
    DELIVERY_TYPE_CHOICES = (
        ('delivery', 'Yetkazib berish'),
        ('pickup', 'Olib ketish'),
    )

    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES)

    address = models.ForeignKey('users.UserAddress', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.JSONField(null=True, blank=True)  # Snapshot

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    coupon = models.ForeignKey('coupons.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)

    customer_note = models.TextField(null=True, blank=True)
    admin_note = models.TextField(null=True, blank=True)

    estimated_delivery = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.order_number


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)

    product_name = models.CharField(max_length=255)  # Snapshot
    product_image = models.CharField(max_length=500, null=True, blank=True)  # Snapshot URL
    sku = models.CharField(max_length=50)

    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)


class OrderStatusHistory(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)