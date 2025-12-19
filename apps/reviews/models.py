from django.db import models
from apps.core.models import BaseModel


class Review(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)

    rating = models.IntegerField()  # 1-5 validation serializerda bo'ladi
    comment = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)

    admin_reply = models.TextField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'product')