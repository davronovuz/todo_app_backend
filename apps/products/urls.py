# project/urls.py  (yoki siz xohlagan yagona urls.py fayli)
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# import your viewsets (yo'llarni loyihangizga moslang)
from .views import CategoryViewSet, ProductViewSet
from .views import TodoViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

# development-da MEDIA fayllarini xizmat qilish (DEBUG=True uchun)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
