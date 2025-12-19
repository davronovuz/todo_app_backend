from django.db import models
from apps.core.models import BaseModel

class WishlistItem(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')