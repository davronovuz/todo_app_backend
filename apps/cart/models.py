from django.db import models
from apps.core.models import BaseModel

class Cart(BaseModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='cart')


    def __str__(self):
        return f"Cart of {self.user.phone}"

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')