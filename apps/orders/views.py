from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, OrderCreateSerializer
from apps.cart.models import Cart
import uuid


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        # Oddiy user faqat o'z buyurtmalarini ko'radi
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        cart = user.cart
        cart_items = cart.items.select_related('product').all()

        data = serializer.validated_data

        # Hisob-kitoblar
        subtotal = sum(item.quantity * item.product.price for item in cart_items)
        delivery_fee = 20000 if data['delivery_type'] == 'delivery' else 0  # Mantiqni o'zgartirish mumkin
        discount = 0  # Kelajakda kupon logikasi shu yerda bo'ladi
        total = subtotal + delivery_fee - discount

        with transaction.atomic():
            # 1. Order yaratish
            order = Order.objects.create(
                user=user,
                order_number=f"HM-{int(timezone.now().timestamp())}",  # Simple ID gen
                status='pending',
                payment_status='pending',
                payment_method=data['payment_method'],
                delivery_type=data['delivery_type'],
                address=data.get('address'),
                # Snapshot address
                delivery_address=UserAddressSerializer(data.get('address')).data if data.get('address') else None,
                subtotal=subtotal,
                discount=discount,
                delivery_fee=delivery_fee,
                total=total,
                customer_note=data.get('customer_note')
            )

            # 2. Order Items yaratish (Snapshot)
            order_items = []
            for item in cart_items:
                order_items.append(OrderItem(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,  # Snapshot name
                    product_image=item.product.images.filter(
                        is_primary=True).first().image.url if item.product.images.exists() else None,
                    sku=item.product.sku,
                    quantity=item.quantity,
                    unit_price=item.product.price,  # Snapshot price
                    total_price=item.quantity * item.product.price
                ))
            OrderItem.objects.bulk_create(order_items)

            # 3. Status History
            OrderStatusHistory.objects.create(
                order=order, status='pending', note='Buyurtma yaratildi'
            )

            # 4. Savatchani tozalash
            cart.items.all().delete()

            # TODO: Send Notification logic here

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status in ['delivered', 'cancelled']:
            return Response({"error": "Buyurtmani bekor qilib bo'lmaydi"}, status=400)

        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()

        OrderStatusHistory.objects.create(order=order, status='cancelled', note='User bekor qildi')
        return Response({"status": "cancelled"})