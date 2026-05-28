from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

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
    create_url_name = ''
    update_url_name = ''
    delete_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['detail_url_name'] = self.detail_url_name
        context['create_url_name'] = self.create_url_name
        context['update_url_name'] = self.update_url_name
        context['delete_url_name'] = self.delete_url_name
        context['model_name'] = self.model._meta.model_name
        return context


class DataDetailMixin:
    template_name = 'restaurant/data_detail.html'
    context_object_name = 'object'
    page_title = ''
    list_url_name = ''
    update_url_name = ''
    delete_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['list_url_name'] = self.list_url_name
        context['update_url_name'] = self.update_url_name
        context['delete_url_name'] = self.delete_url_name
        context['model_name'] = self.model._meta.model_name
        return context


class DataFormMixin:
    template_name = 'restaurant/data_form.html'
    page_title = ''
    list_url_name = ''

    def get_success_url(self):
        return reverse_lazy(self.list_url_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['list_url_name'] = self.list_url_name
        return context


class DataDeleteMixin:
    template_name = 'restaurant/data_confirm_delete.html'
    page_title = ''
    list_url_name = ''

    def get_success_url(self):
        return reverse_lazy(self.list_url_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['list_url_name'] = self.list_url_name
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
    create_url_name = 'category_create'
    update_url_name = 'category_update'
    delete_url_name = 'category_delete'


class CategoryDetailView(DataDetailMixin, DetailView):
    model = Category
    page_title = 'Категория'
    list_url_name = 'category_list'
    update_url_name = 'category_update'
    delete_url_name = 'category_delete'


class CategoryCreateView(DataFormMixin, CreateView):
    model = Category
    fields = ['name', 'slug', 'description', 'is_active']
    page_title = 'Добавить категорию'
    list_url_name = 'category_list'


class CategoryUpdateView(DataFormMixin, UpdateView):
    model = Category
    fields = ['name', 'slug', 'description', 'is_active']
    page_title = 'Изменить категорию'
    list_url_name = 'category_list'


class CategoryDeleteView(DataDeleteMixin, DeleteView):
    model = Category
    page_title = 'Удалить категорию'
    list_url_name = 'category_list'


class MenuItemDataListView(DataListMixin, ListView):
    model = MenuItem
    page_title = 'Блюда меню'
    detail_url_name = 'menu_item_data_detail'
    create_url_name = 'menu_item_create'
    update_url_name = 'menu_item_update'
    delete_url_name = 'menu_item_delete'

    def get_queryset(self):
        return MenuItem.objects.select_related('category')


class MenuItemDataDetailView(DataDetailMixin, DetailView):
    model = MenuItem
    page_title = 'Блюдо меню'
    list_url_name = 'menu_item_data_list'
    update_url_name = 'menu_item_update'
    delete_url_name = 'menu_item_delete'

    def get_queryset(self):
        return MenuItem.objects.select_related('category')


class MenuItemCreateView(DataFormMixin, CreateView):
    model = MenuItem
    fields = ['category', 'name', 'slug', 'composition', 'image', 'price', 'weight_grams', 'is_available']
    page_title = 'Добавить блюдо'
    list_url_name = 'menu_item_data_list'


class MenuItemUpdateView(DataFormMixin, UpdateView):
    model = MenuItem
    fields = ['category', 'name', 'slug', 'composition', 'image', 'price', 'weight_grams', 'is_available']
    page_title = 'Изменить блюдо'
    list_url_name = 'menu_item_data_list'


class MenuItemDeleteView(DataDeleteMixin, DeleteView):
    model = MenuItem
    page_title = 'Удалить блюдо'
    list_url_name = 'menu_item_data_list'


class OrderListView(DataListMixin, ListView):
    model = Order
    page_title = 'Заказы'
    detail_url_name = 'order_detail'
    create_url_name = 'order_create'
    update_url_name = 'order_update'
    delete_url_name = 'order_delete'

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderDetailView(DataDetailMixin, DetailView):
    model = Order
    page_title = 'Заказ'
    list_url_name = 'order_list'
    update_url_name = 'order_update'
    delete_url_name = 'order_delete'

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderCreateView(DataFormMixin, CreateView):
    model = Order
    fields = [
        'user',
        'delivery_city',
        'delivery_street',
        'delivery_building',
        'delivery_apartment',
        'delivery_comment',
        'status',
        'comment',
    ]
    page_title = 'Добавить заказ'
    list_url_name = 'order_list'


class OrderUpdateView(DataFormMixin, UpdateView):
    model = Order
    fields = [
        'user',
        'delivery_city',
        'delivery_street',
        'delivery_building',
        'delivery_apartment',
        'delivery_comment',
        'status',
        'comment',
    ]
    page_title = 'Изменить заказ'
    list_url_name = 'order_list'


class OrderDeleteView(DataDeleteMixin, DeleteView):
    model = Order
    page_title = 'Удалить заказ'
    list_url_name = 'order_list'


class OrderItemListView(DataListMixin, ListView):
    model = OrderItem
    page_title = 'Состав заказов'
    detail_url_name = 'order_item_detail'
    create_url_name = 'order_item_create'
    update_url_name = 'order_item_update'
    delete_url_name = 'order_item_delete'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'menu_item')


class OrderItemDetailView(DataDetailMixin, DetailView):
    model = OrderItem
    page_title = 'Позиция заказа'
    list_url_name = 'order_item_list'
    update_url_name = 'order_item_update'
    delete_url_name = 'order_item_delete'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'menu_item')


class OrderItemCreateView(DataFormMixin, CreateView):
    model = OrderItem
    fields = ['order', 'menu_item', 'quantity', 'unit_price']
    page_title = 'Добавить позицию заказа'
    list_url_name = 'order_item_list'


class OrderItemUpdateView(DataFormMixin, UpdateView):
    model = OrderItem
    fields = ['order', 'menu_item', 'quantity', 'unit_price']
    page_title = 'Изменить позицию заказа'
    list_url_name = 'order_item_list'


class OrderItemDeleteView(DataDeleteMixin, DeleteView):
    model = OrderItem
    page_title = 'Удалить позицию заказа'
    list_url_name = 'order_item_list'


class PaymentListView(DataListMixin, ListView):
    model = Payment
    page_title = 'Оплаты'
    detail_url_name = 'payment_detail'
    create_url_name = 'payment_create'
    update_url_name = 'payment_update'
    delete_url_name = 'payment_delete'

    def get_queryset(self):
        return Payment.objects.select_related('order')


class PaymentDetailView(DataDetailMixin, DetailView):
    model = Payment
    page_title = 'Оплата'
    list_url_name = 'payment_list'
    update_url_name = 'payment_update'
    delete_url_name = 'payment_delete'

    def get_queryset(self):
        return Payment.objects.select_related('order')


class PaymentCreateView(DataFormMixin, CreateView):
    model = Payment
    fields = ['order', 'method', 'amount', 'is_paid', 'paid_at']
    page_title = 'Добавить оплату'
    list_url_name = 'payment_list'


class PaymentUpdateView(DataFormMixin, UpdateView):
    model = Payment
    fields = ['order', 'method', 'amount', 'is_paid', 'paid_at']
    page_title = 'Изменить оплату'
    list_url_name = 'payment_list'


class PaymentDeleteView(DataDeleteMixin, DeleteView):
    model = Payment
    page_title = 'Удалить оплату'
    list_url_name = 'payment_list'


class FavoriteListView(DataListMixin, ListView):
    model = Favorite
    page_title = 'Избранное'
    detail_url_name = 'favorite_detail'
    create_url_name = 'favorite_create'
    update_url_name = 'favorite_update'
    delete_url_name = 'favorite_delete'

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'menu_item')


class FavoriteDetailView(DataDetailMixin, DetailView):
    model = Favorite
    page_title = 'Избранное'
    list_url_name = 'favorite_list'
    update_url_name = 'favorite_update'
    delete_url_name = 'favorite_delete'

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'menu_item')


class FavoriteCreateView(DataFormMixin, CreateView):
    model = Favorite
    fields = ['user', 'menu_item']
    page_title = 'Добавить в избранное'
    list_url_name = 'favorite_list'


class FavoriteUpdateView(DataFormMixin, UpdateView):
    model = Favorite
    fields = ['user', 'menu_item']
    page_title = 'Изменить избранное'
    list_url_name = 'favorite_list'


class FavoriteDeleteView(DataDeleteMixin, DeleteView):
    model = Favorite
    page_title = 'Удалить избранное'
    list_url_name = 'favorite_list'


class ReviewListView(DataListMixin, ListView):
    model = Review
    page_title = 'Отзывы'
    detail_url_name = 'review_detail'
    create_url_name = 'review_create'
    update_url_name = 'review_update'
    delete_url_name = 'review_delete'

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item')


class ReviewDetailView(DataDetailMixin, DetailView):
    model = Review
    page_title = 'Отзыв'
    list_url_name = 'review_list'
    update_url_name = 'review_update'
    delete_url_name = 'review_delete'

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item')


class ReviewCreateView(DataFormMixin, CreateView):
    model = Review
    fields = ['user', 'menu_item', 'rating', 'text', 'image', 'is_published']
    page_title = 'Добавить отзыв'
    list_url_name = 'review_list'


class ReviewUpdateView(DataFormMixin, UpdateView):
    model = Review
    fields = ['user', 'menu_item', 'rating', 'text', 'image', 'is_published']
    page_title = 'Изменить отзыв'
    list_url_name = 'review_list'


class ReviewDeleteView(DataDeleteMixin, DeleteView):
    model = Review
    page_title = 'Удалить отзыв'
    list_url_name = 'review_list'
