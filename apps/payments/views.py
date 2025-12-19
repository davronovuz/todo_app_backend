from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import PaymentSerializer, CreatePaymentSerializer
from apps.orders.models import Order


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        provider = serializer.validated_data['provider']

        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.payment_status == 'paid':
            return Response({"error": "Bu buyurtma allaqachon to'langan"}, status=400)

        # Payment obyekti yaratiladi
        payment = Payment.objects.create(
            order=order,
            provider=provider,
            amount=order.total,
            status='pending'
        )

        # Bu yerda Providerdan (Payme/Click) URL generatsiya qilish logikasi bo'ladi
        payment_url = f"https://checkout.{provider}.uz/..."

        return Response({
            "payment_id": payment.id,
            "payment_url": payment_url,
            "amount": payment.amount
        })

    # Webhooklar uchun (Auth talab qilinmaydi, IP whitelist qilinadi)
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='payme-webhook')
    def payme_webhook(self, request):
        # Payme logikasi: Transaction tekshirish, status o'zgartirish
        # Bu yerda Payme hujjatlariga qarab Merchant API yoziladi
        return Response({"result": "success"})  # Placeholder

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='click-webhook')
    def click_webhook(self, request):
        # Click logikasi: Prepare/Complete metodlari
        return Response({"result": "success"})  # Placeholder