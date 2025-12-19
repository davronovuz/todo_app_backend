from rest_framework import serializers
from .models import Review
from apps.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'order', 'rating', 'comment', 'created_at')
        read_only_fields = ('user', 'is_verified', 'is_approved', 'admin_reply')

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Reyting 1 va 5 oralig'ida bo'lishi kerak")
        return value