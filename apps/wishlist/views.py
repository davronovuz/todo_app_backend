from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from apps.cart.models import Cart, CartItem
from apps.products.models import Product


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def move_to_cart(self, request, pk=None):
        wishlist_item = self.get_object()
        product = wishlist_item.product

        # Savatchaga qo'shish
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Wishlistdan o'chirish
        wishlist_item.delete()

        return Response({"message": "Mahsulot savatchaga o'tkazildi"}, status=status.HTTP_200_OK)