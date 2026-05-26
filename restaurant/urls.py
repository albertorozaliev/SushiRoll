from django.urls import path

from . import views

urlpatterns = [
    path('', views.InformationView.as_view(), name='information'),
    path('products/', views.MenuItemListView.as_view(), name='products'),
    path('products/<int:pk>/', views.MenuItemDetailView.as_view(), name='product_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('data/', views.DataIndexView.as_view(), name='data_index'),
    path('data/users/', views.UserListView.as_view(), name='user_list'),
    path('data/users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('data/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('data/categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('data/menu-items/', views.MenuItemDataListView.as_view(), name='menu_item_data_list'),
    path('data/menu-items/<int:pk>/', views.MenuItemDataDetailView.as_view(), name='menu_item_data_detail'),
    path('data/orders/', views.OrderListView.as_view(), name='order_list'),
    path('data/orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('data/order-items/', views.OrderItemListView.as_view(), name='order_item_list'),
    path('data/order-items/<int:pk>/', views.OrderItemDetailView.as_view(), name='order_item_detail'),
    path('data/payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('data/payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('data/favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    path('data/favorites/<int:pk>/', views.FavoriteDetailView.as_view(), name='favorite_detail'),
    path('data/reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('data/reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
]
