from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    CategoryViewSet,
    FavoriteViewSet,
    MenuItemViewSet,
    OrderItemViewSet,
    OrderViewSet,
    PaymentViewSet,
    ReviewViewSet,
    UserProfileViewSet,
    UserViewSet,
)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('menu-items', MenuItemViewSet)
router.register('user-profiles', UserProfileViewSet)
router.register('orders', OrderViewSet)
router.register('order-items', OrderItemViewSet)
router.register('payments', PaymentViewSet)
router.register('favorites', FavoriteViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
