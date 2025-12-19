from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'updated_at')
    search_fields = ('product__name', 'product__sku')
    list_editable = ('quantity',) # Ro'yxatni o'zidan o'zgartirish imkoniyati