from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Coupon
from .serializers import CouponSerializer, CouponValidateSerializer


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.filter(is_active=True, end_date__gte=timezone.now())
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def validate_code(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        amount = serializer.validated_data['order_amount']

        try:
            coupon = Coupon.objects.get(
                code=code,
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
        except Coupon.DoesNotExist:
            return Response({"error": "Kupon topilmadi yoki muddati tugagan"}, status=400)

        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            return Response({"error": "Kupon limiti tugagan"}, status=400)

        if coupon.min_order_amount and amount < coupon.min_order_amount:
            return Response({
                "error": f"Minimal buyurtma summasi: {coupon.min_order_amount}"
            }, status=400)

        return Response(CouponSerializer(coupon).data)