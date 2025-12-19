from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductTag


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'icon', 'children')

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_primary')


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ('id', 'name', 'color')


class ProductListSerializer(serializers.ModelSerializer):
    # Ro'yxat uchun yengil serializer
    category = serializers.CharField(source='category.name')
    brand = serializers.CharField(source='brand.name', allow_null=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'price', 'old_price',
            'category', 'brand', 'primary_image',
            'avg_rating', 'review_count', 'is_active'
        )

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first()
        if img:
            return img.image.url
        first_img = obj.images.first()
        return first_img.image.url if first_img else None


class ProductDetailSerializer(serializers.ModelSerializer):
    # Bitta mahsulot uchun to'liq serializer
    category = CategorySerializer()
    brand = BrandSerializer()
    images = ProductImageSerializer(many=True)
    tags = ProductTagSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'