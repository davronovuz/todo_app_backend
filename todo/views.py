from django.shortcuts import render
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
import mimetypes

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all().order_by('-id')
    serializer_class = ProductSerializer

    # extra endpoint to return binary image (so client can GET /api/products/{pk}/image/)
    @action(detail=True, methods=['get'])
    def image(self, request, pk=None):
        product = self.get_object()
        if not product.image:
            raise Http404("Image not found")
        # open the file and return FileResponse with guessed mimetype
        mime, _ = mimetypes.guess_type(product.image.path)
        mime = mime or 'application/octet-stream'
        return FileResponse(product.image.open('rb'), content_type=mime)
