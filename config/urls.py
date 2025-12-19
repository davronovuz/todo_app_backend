from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Viewlarni import qilamiz
from apps.users.views import AuthViewSet, UserViewSet, AddressViewSet
from apps.products.views import CategoryViewSet, BrandViewSet, ProductViewSet
from apps.cart.views import CartViewSet
from apps.orders.views import OrderViewSet
from apps.payments.views import PaymentViewSet

# Qolgan Viewlar (Bularni hali yozmagan bo'lsangiz, kommentariyada turgani ma'qul)
from apps.reviews.views import ReviewViewSet
from apps.wishlist.views import WishlistViewSet
from apps.coupons.views import CouponViewSet
from apps.notifications.views import NotificationViewSet

# -----------------------------------------------------------------------------
# Swagger (API Documentation) sozlamalari
# -----------------------------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Halol Market API",
        default_version='v1',
        description="Halol Market e-commerce loyihasi uchun REST API hujjatlari",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@halolmarket.uz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# -----------------------------------------------------------------------------
# Router (Avtomatik URL generatsiya)
# -----------------------------------------------------------------------------
router = DefaultRouter()

# Users & Auth
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')
router.register(r'addresses', AddressViewSet, basename='addresses')

# Products
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'products', ProductViewSet, basename='products')

# Cart
router.register(r'cart', CartViewSet, basename='cart')

# Orders
router.register(r'orders', OrderViewSet, basename='orders')

# Payments
router.register(r'payments', PaymentViewSet, basename='payments')

# Boshqa ilovalar (Viewlarni yozganingizdan keyin kommentdan chiqaring)
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'coupons', CouponViewSet, basename='coupons')
router.register(r'notifications', NotificationViewSet, basename='notifications')

# -----------------------------------------------------------------------------
# URL Patterns
# -----------------------------------------------------------------------------
urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Asosiy API (v1)
    path('api/v1/', include(router.urls)),

    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# -----------------------------------------------------------------------------
# Media & Static (Faqat DEBUG rejimida)
# -----------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)