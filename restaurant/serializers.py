from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Favorite, MenuItem, Order, OrderItem, Payment, Review, UserProfile


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined',
            'password',
        ]
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'category',
            'category_name',
            'name',
            'slug',
            'composition',
            'image',
            'price',
            'weight_grams',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'category_name', 'slug', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'photo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'username',
            'delivery_city',
            'delivery_street',
            'delivery_building',
            'delivery_apartment',
            'delivery_comment',
            'status',
            'status_display',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'username', 'status_display', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    order_number = serializers.IntegerField(source='order.id', read_only=True)
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'order_number', 'menu_item', 'menu_item_name', 'quantity', 'unit_price']
        read_only_fields = ['id', 'order_number', 'menu_item_name']


class PaymentSerializer(serializers.ModelSerializer):
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'method_display', 'amount', 'is_paid', 'paid_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'method_display', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'username', 'menu_item', 'menu_item_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'menu_item_name', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'username',
            'menu_item',
            'menu_item_name',
            'rating',
            'text',
            'image',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'username', 'menu_item_name', 'created_at', 'updated_at']
