import uuid  # <--- 1. BU IMPORT QO'SHILDI
from django.db import models
from apps.core.models import BaseModel


class Category(BaseModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100, null=True, blank=True)
    name_ru = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    name = models.CharField(max_length=255)
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)

    description = models.TextField()
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    unit = models.CharField(max_length=20, default='dona')
    unit_value = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_halal_certified = models.BooleanField(default=True)

    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    review_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    # --- XATO TUZATILDI ---
    # Eski (Xato): default=models.UUIDField
    # Yangi (To'g'ri): default=uuid.uuid4
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)


class ProductTag(BaseModel):
    products = models.ManyToManyField(Product, related_name='tags')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    color = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.name