from django.contrib import admin
from .models import Coupon, CouponUsage

class CouponUsageInline(admin.TabularInline):
    model = CouponUsage
    extra = 0
    readonly_fields = ('created_at',)
    can_delete = False

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'value', 'start_date', 'end_date', 'is_active', 'used_count')
    list_filter = ('type', 'is_active', 'start_date', 'end_date')
    search_fields = ('code', 'name')
    inlines = [CouponUsageInline]