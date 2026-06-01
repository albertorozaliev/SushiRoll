from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from .models import Category, Favorite, MenuItem, Order, OrderItem, Payment, Review, UserProfile
from .permissions import IsStaffOrReadOnly
from .serializers import (
    CategorySerializer,
    FavoriteSerializer,
    MenuItemSerializer,
    OrderItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    ReviewSerializer,
    UserProfileSerializer,
    UserSerializer,
)


User = get_user_model()


class BaseApiViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]


class UserViewSet(BaseApiViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email', 'date_joined']


class CategoryViewSet(BaseApiViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name', 'slug', 'description']
    ordering_fields = ['id', 'name', 'created_at']


class MenuItemViewSet(BaseApiViewSet):
    queryset = MenuItem.objects.select_related('category')
    serializer_class = MenuItemSerializer
    search_fields = ['name', 'slug', 'composition', 'category__name']
    ordering_fields = ['id', 'name', 'price', 'weight_grams', 'created_at']


class UserProfileViewSet(BaseApiViewSet):
    queryset = UserProfile.objects.select_related('user')
    serializer_class = UserProfileSerializer
    search_fields = ['user__username', 'user__email']
    ordering_fields = ['id', 'created_at']


class OrderViewSet(BaseApiViewSet):
    queryset = Order.objects.select_related('user')
    serializer_class = OrderSerializer
    search_fields = [
        'user__username',
        'user__email',
        'delivery_city',
        'delivery_street',
        'delivery_building',
        'delivery_apartment',
        'delivery_comment',
        'status',
        'comment',
    ]
    ordering_fields = ['id', 'created_at', 'status', 'delivery_city']


class OrderItemViewSet(BaseApiViewSet):
    queryset = OrderItem.objects.select_related('order', 'menu_item')
    serializer_class = OrderItemSerializer
    search_fields = ['menu_item__name']
    ordering_fields = ['id', 'order', 'menu_item', 'quantity', 'unit_price']


class PaymentViewSet(BaseApiViewSet):
    queryset = Payment.objects.select_related('order')
    serializer_class = PaymentSerializer
    search_fields = ['method']
    ordering_fields = ['id', 'order', 'amount', 'paid_at', 'created_at']


class FavoriteViewSet(BaseApiViewSet):
    queryset = Favorite.objects.select_related('user', 'menu_item')
    serializer_class = FavoriteSerializer
    search_fields = ['user__username', 'user__email', 'menu_item__name']
    ordering_fields = ['id', 'user', 'menu_item', 'created_at']


class ReviewViewSet(BaseApiViewSet):
    queryset = Review.objects.select_related('user', 'menu_item')
    serializer_class = ReviewSerializer
    search_fields = ['user__username', 'user__email', 'menu_item__name', 'text']
    ordering_fields = ['id', 'rating', 'created_at']
