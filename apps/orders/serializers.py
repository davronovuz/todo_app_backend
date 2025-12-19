from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from apps.cart.models import Cart
from apps.users.serializers import UserAddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id', 'product', 'product_name', 'product_image',
            'sku', 'quantity', 'unit_price', 'total_price'
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = serializers.JSONField()  # Read-only snapshot

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'user', 'order_number', 'status', 'payment_status',
            'subtotal', 'discount', 'total', 'created_at'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(write_only=True, required=False)  # Agar kelajakda guest checkout bo'lsa

    class Meta:
        model = Order
        fields = (
            'payment_method', 'delivery_type', 'address',
            'customer_note', 'coupon_code', 'cart_id'
        )

    def validate(self, attrs):
        user = self.context['request'].user
        if not hasattr(user, 'cart') or not user.cart.items.exists():
            raise serializers.ValidationError("Savatchangiz bo'sh!")

        if attrs['delivery_type'] == 'delivery' and not attrs.get('address'):
            raise serializers.ValidationError("Yetkazib berish uchun manzil tanlanishi shart.")

        return attrs