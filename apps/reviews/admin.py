from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_approved', 'is_verified', 'created_at')
    list_filter = ('is_approved', 'rating', 'is_verified')
    search_fields = ('user__phone', 'product__name', 'comment')
    list_editable = ('is_approved',) # Admin panel ro'yxatidan tasdiqlash