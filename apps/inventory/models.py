from django.db import models
from apps.core.models import BaseModel


class Stock(BaseModel):
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE, related_name='stock')
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    # Qo'shimcha (ixtiyoriy, agar har bir ombor uchun kerak bo'lsa)
    # warehouse_id ...

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"