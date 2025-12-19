from rest_framework import serializers
from django.utils import timezone
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'code', 'type', 'value', 'min_order_amount', 'end_date')

class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)
    order_amount = serializers.DecimalField(max_digits=12, decimal_places=2)