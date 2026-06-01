from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import RegisterForm, StaffUserCreateForm, StaffUserUpdateForm
from .models import Category, Favorite, MenuItem, Order, OrderItem, Payment, Review


User = get_user_model()


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        raise PermissionDenied


class SiteLoginView(LoginView):
    template_name = 'auth_form.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Вход'
        context['submit_label'] = 'Войти'
        context['secondary_url_name'] = 'register'
        context['secondary_label'] = 'Зарегистрироваться'
        return context


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth_form.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Регистрация'
        context['submit_label'] = 'Зарегистрироваться'
        context['secondary_url_name'] = 'login'
        context['secondary_label'] = 'Уже есть аккаунт'
        return context


class ProfileView(TemplateView):
    template_name = 'profile.html'


class SiteLogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('information')


class InformationView(TemplateView):
    template_name = 'information.html'


class CartView(TemplateView):
    template_name = 'cart.html'


class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'products.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        self.categories = Category.objects.filter(is_active=True)
        category_slug = self.request.GET.get('category')
        selected_category = None

        if category_slug:
            selected_category = self.categories.filter(slug=category_slug).first()

        if selected_category is None:
            selected_category = self.categories.first()

        self.selected_category = selected_category

        if selected_category is None:
            return MenuItem.objects.none()

        return selected_category.menu_items.filter(is_available=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        context['selected_category'] = self.selected_category
        context['selected_category_name'] = self.selected_category.name if self.selected_category else 'меню'
        return context


class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'product_detail.html'
    context_object_name = 'menu_item'

    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True).select_related('category')


class DataIndexView(StaffRequiredMixin, TemplateView):
    template_name = 'data_index.html'


class DataListMixin:
    template_name = 'data_list.html'
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
    template_name = 'data_detail.html'
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
    template_name = 'data_form.html'
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
    template_name = 'data_confirm_delete.html'
    page_title = ''
    list_url_name = ''

    def get_success_url(self):
        return reverse_lazy(self.list_url_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['list_url_name'] = self.list_url_name
        return context


class UserListView(StaffRequiredMixin, DataListMixin, ListView):
    model = User
    page_title = 'Пользователи'
    detail_url_name = 'user_detail'
    create_url_name = 'user_create'
    update_url_name = 'user_update'
    delete_url_name = 'user_delete'

    def get_queryset(self):
        return User.objects.select_related('profile')


class UserDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = User
    page_title = 'Пользователь'
    list_url_name = 'user_list'
    update_url_name = 'user_update'
    delete_url_name = 'user_delete'

    def get_queryset(self):
        return User.objects.select_related('profile')


class UserCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = User
    form_class = StaffUserCreateForm
    page_title = 'Добавить пользователя'
    list_url_name = 'user_list'


class UserUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = User
    form_class = StaffUserUpdateForm
    page_title = 'Изменить пользователя'
    list_url_name = 'user_list'


class UserDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = User
    page_title = 'Удалить пользователя'
    list_url_name = 'user_list'


class CategoryListView(StaffRequiredMixin, DataListMixin, ListView):
    model = Category
    page_title = 'Категории'
    detail_url_name = 'category_detail'
    create_url_name = 'category_create'
    update_url_name = 'category_update'
    delete_url_name = 'category_delete'


class CategoryDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = Category
    page_title = 'Категория'
    list_url_name = 'category_list'
    update_url_name = 'category_update'
    delete_url_name = 'category_delete'


class CategoryCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = Category
    fields = ['name', 'description', 'is_active']
    page_title = 'Добавить категорию'
    list_url_name = 'category_list'


class CategoryUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'is_active']
    page_title = 'Изменить категорию'
    list_url_name = 'category_list'


class CategoryDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = Category
    page_title = 'Удалить категорию'
    list_url_name = 'category_list'


class MenuItemDataListView(StaffRequiredMixin, DataListMixin, ListView):
    model = MenuItem
    page_title = 'Блюда меню'
    detail_url_name = 'menu_item_data_detail'
    create_url_name = 'menu_item_create'
    update_url_name = 'menu_item_update'
    delete_url_name = 'menu_item_delete'

    def get_queryset(self):
        return MenuItem.objects.select_related('category')


class MenuItemDataDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = MenuItem
    page_title = 'Блюдо меню'
    list_url_name = 'menu_item_data_list'
    update_url_name = 'menu_item_update'
    delete_url_name = 'menu_item_delete'

    def get_queryset(self):
        return MenuItem.objects.select_related('category')


class MenuItemCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = MenuItem
    fields = ['category', 'name', 'composition', 'image', 'price', 'weight_grams', 'is_available']
    page_title = 'Добавить блюдо'
    list_url_name = 'menu_item_data_list'


class MenuItemUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = MenuItem
    fields = ['category', 'name', 'composition', 'image', 'price', 'weight_grams', 'is_available']
    page_title = 'Изменить блюдо'
    list_url_name = 'menu_item_data_list'


class MenuItemDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = MenuItem
    page_title = 'Удалить блюдо'
    list_url_name = 'menu_item_data_list'


class OrderListView(StaffRequiredMixin, DataListMixin, ListView):
    model = Order
    page_title = 'Заказы'
    detail_url_name = 'order_detail'
    create_url_name = 'order_create'
    update_url_name = 'order_update'
    delete_url_name = 'order_delete'

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = Order
    page_title = 'Заказ'
    list_url_name = 'order_list'
    update_url_name = 'order_update'
    delete_url_name = 'order_delete'

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
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


class OrderUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
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


class OrderDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = Order
    page_title = 'Удалить заказ'
    list_url_name = 'order_list'


class OrderItemListView(StaffRequiredMixin, DataListMixin, ListView):
    model = OrderItem
    page_title = 'Состав заказов'
    detail_url_name = 'order_item_detail'
    create_url_name = 'order_item_create'
    update_url_name = 'order_item_update'
    delete_url_name = 'order_item_delete'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'menu_item')


class OrderItemDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = OrderItem
    page_title = 'Позиция заказа'
    list_url_name = 'order_item_list'
    update_url_name = 'order_item_update'
    delete_url_name = 'order_item_delete'

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'menu_item')


class OrderItemCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = OrderItem
    fields = ['order', 'menu_item', 'quantity', 'unit_price']
    page_title = 'Добавить позицию заказа'
    list_url_name = 'order_item_list'


class OrderItemUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = OrderItem
    fields = ['order', 'menu_item', 'quantity', 'unit_price']
    page_title = 'Изменить позицию заказа'
    list_url_name = 'order_item_list'


class OrderItemDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = OrderItem
    page_title = 'Удалить позицию заказа'
    list_url_name = 'order_item_list'


class PaymentListView(StaffRequiredMixin, DataListMixin, ListView):
    model = Payment
    page_title = 'Оплаты'
    detail_url_name = 'payment_detail'
    create_url_name = 'payment_create'
    update_url_name = 'payment_update'
    delete_url_name = 'payment_delete'

    def get_queryset(self):
        return Payment.objects.select_related('order')


class PaymentDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = Payment
    page_title = 'Оплата'
    list_url_name = 'payment_list'
    update_url_name = 'payment_update'
    delete_url_name = 'payment_delete'

    def get_queryset(self):
        return Payment.objects.select_related('order')


class PaymentCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = Payment
    fields = ['order', 'method', 'amount', 'is_paid', 'paid_at']
    page_title = 'Добавить оплату'
    list_url_name = 'payment_list'


class PaymentUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = Payment
    fields = ['order', 'method', 'amount', 'is_paid', 'paid_at']
    page_title = 'Изменить оплату'
    list_url_name = 'payment_list'


class PaymentDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = Payment
    page_title = 'Удалить оплату'
    list_url_name = 'payment_list'


class FavoriteListView(StaffRequiredMixin, DataListMixin, ListView):
    model = Favorite
    page_title = 'Избранное'
    detail_url_name = 'favorite_detail'
    create_url_name = 'favorite_create'
    update_url_name = 'favorite_update'
    delete_url_name = 'favorite_delete'

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'menu_item')


class FavoriteDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = Favorite
    page_title = 'Избранное'
    list_url_name = 'favorite_list'
    update_url_name = 'favorite_update'
    delete_url_name = 'favorite_delete'

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'menu_item')


class FavoriteCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = Favorite
    fields = ['user', 'menu_item']
    page_title = 'Добавить в избранное'
    list_url_name = 'favorite_list'


class FavoriteUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = Favorite
    fields = ['user', 'menu_item']
    page_title = 'Изменить избранное'
    list_url_name = 'favorite_list'


class FavoriteDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = Favorite
    page_title = 'Удалить избранное'
    list_url_name = 'favorite_list'


class ReviewListView(StaffRequiredMixin, DataListMixin, ListView):
    model = Review
    page_title = 'Отзывы'
    detail_url_name = 'review_detail'
    create_url_name = 'review_create'
    update_url_name = 'review_update'
    delete_url_name = 'review_delete'

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item')


class ReviewDetailView(StaffRequiredMixin, DataDetailMixin, DetailView):
    model = Review
    page_title = 'Отзыв'
    list_url_name = 'review_list'
    update_url_name = 'review_update'
    delete_url_name = 'review_delete'

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item')


class ReviewCreateView(StaffRequiredMixin, DataFormMixin, CreateView):
    model = Review
    fields = ['user', 'menu_item', 'rating', 'text', 'image', 'is_published']
    page_title = 'Добавить отзыв'
    list_url_name = 'review_list'


class ReviewUpdateView(StaffRequiredMixin, DataFormMixin, UpdateView):
    model = Review
    fields = ['user', 'menu_item', 'rating', 'text', 'image', 'is_published']
    page_title = 'Изменить отзыв'
    list_url_name = 'review_list'


class ReviewDeleteView(StaffRequiredMixin, DataDeleteMixin, DeleteView):
    model = Review
    page_title = 'Удалить отзыв'
    list_url_name = 'review_list'
