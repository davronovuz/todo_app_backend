from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']



from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, allow_null=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=True
    )

    class Meta:
        model = Product
        fields = "__all__"

