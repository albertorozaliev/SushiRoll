from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Favorite, MenuItem, Order, OrderItem, Payment, Review


User = get_user_model()


class InformationView(TemplateView):
    template_name = 'restaurant/information.html'


class CartView(TemplateView):
    template_name = 'restaurant/cart.html'


class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'restaurant/products.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        category = self.request.GET.get('category', 'rolls')
        category_names = {
            'rolls': 'Роллы',
            'sushi': 'Суши',
        }
        selected_category_name = category_names.get(category, category_names['rolls'])
        self.selected_category = category
        self.selected_category_name = selected_category_name

        return MenuItem.objects.filter(
            is_available=True,
            category__name__iexact=selected_category_name,
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.selected_category
        context['selected_category_name'] = self.selected_category_name
        return context


class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'restaurant/product_detail.html'
    context_object_name = 'menu_item'

    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True).select_related('category')


class DataIndexView(TemplateView):
    template_name = 'restaurant/data_index.html'


class DataListMixin:
    template_name = 'restaurant/data_list.html'
    context_object_name = 'objects'
    page_title = ''
    detail_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['detail_url_name'] = self.detail_url_name
        context['model_name'] = self.model._meta.model_name
        return context


class DataDetailMixin:
    template_name = 'restaurant/data_detail.html'
    context_object_name = 'object'
    page_title = ''
    list_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['list_url_name'] = self.list_url_name
        context['model_name'] = self.model._meta.model_name
        return context


class UserListView(DataListMixin, ListView):
    model = User
    page_title = 'Пользователи'
    detail_url_name = 'user_detail'

    def get_queryset(self):
        return User.objects.select_related('profile')


class UserDetailView(DataDetailMixin, DetailView):
    model = User
    page_title = 'Пользователь'
    list_url_name = 'user_list'

    def get_queryset(self):
        return User.objects.select_related('profile')


class CategoryListView(DataListMixin, ListView):
    model = Category
    page_title = 'Категории'
    detail_url_name = 'category_detail'


class CategoryDetailView(DataDetailMixin, DetailView):
    model = Category
    page_title = 'Категория'
    list_url_name = 'category_list'


class MenuItemDataListView(DataListMixin, ListView):
    model = MenuItem
    page_title = 'Блюда меню'
    detail_url_name = 'menu_item_data_detail'

    def get_queryset(self):
        return MenuItem.objects.select_related('category')


class MenuItemDataDetailView(DataDetailMixin, DetailView):
    model = MenuItem
    page_title = 'Блюдо меню'
    list_url_name = 'menu_item_data_list'

    def get_queryset(self):
        return MenuItem.objects.select_related('category')


class OrderListView(DataListMixin, ListView):
    model = Order
    page_title = 'Заказы'
    detail_url_name = 'order_detail'

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderDetailView(DataDetailMixin, DetailView):
    model = Order
    page_title = 'Заказ'
    list_url_name = 'order_list'

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderItemListView(DataListMixin, ListView):
    model = OrderItem
    page_title = 'Состав заказов'
    detail_url_name = 'order_item_detail'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'menu_item')


class OrderItemDetailView(DataDetailMixin, DetailView):
    model = OrderItem
    page_title = 'Позиция заказа'
    list_url_name = 'order_item_list'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'menu_item')


class PaymentListView(DataListMixin, ListView):
    model = Payment
    page_title = 'Оплаты'
    detail_url_name = 'payment_detail'

    def get_queryset(self):
        return Payment.objects.select_related('order')


class PaymentDetailView(DataDetailMixin, DetailView):
    model = Payment
    page_title = 'Оплата'
    list_url_name = 'payment_list'

    def get_queryset(self):
        return Payment.objects.select_related('order')


class FavoriteListView(DataListMixin, ListView):
    model = Favorite
    page_title = 'Избранное'
    detail_url_name = 'favorite_detail'

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'menu_item')


class FavoriteDetailView(DataDetailMixin, DetailView):
    model = Favorite
    page_title = 'Избранное'
    list_url_name = 'favorite_list'

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'menu_item')


class ReviewListView(DataListMixin, ListView):
    model = Review
    page_title = 'Отзывы'
    detail_url_name = 'review_detail'

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item')


class ReviewDetailView(DataDetailMixin, DetailView):
    model = Review
    page_title = 'Отзыв'
    list_url_name = 'review_list'

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item')
