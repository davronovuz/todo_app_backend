from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'sku', 'unit_price', 'total_price')
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'created_at', 'created_by')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'delivery_type', 'created_at')
    search_fields = ('order_number', 'user__phone', 'user__first_name')
    readonly_fields = ('subtotal', 'discount', 'delivery_fee', 'total', 'created_at')
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    fieldsets = (
        ("Asosiy", {"fields": ("order_number", "user", "status", "created_at")}),
        ("To'lov va Yetkazish",
         {"fields": ("payment_method", "payment_status", "delivery_type", "estimated_delivery")}),
        ("Manzil", {"fields": ("address", "delivery_address")}),
        ("Hisob-kitob", {"fields": ("subtotal", "delivery_fee", "discount", "total")}),
        ("Izohlar", {"fields": ("customer_note", "admin_note", "cancel_reason")}),
    )