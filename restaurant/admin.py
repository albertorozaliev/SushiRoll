from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import (
    Category,
    Favorite,
    MenuItem,
    Order,
    OrderItem,
    Payment,
    Review,
    UserProfile,
)


User = get_user_model()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight_grams', 'is_available')
    list_filter = ('category', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'composition')
    fields = ('category', 'name', 'slug', 'composition', 'image', 'price', 'weight_grams', 'is_available')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    search_fields = ('user__username', 'user__email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_city', 'delivery_street', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'delivery_street', 'delivery_building')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'unit_price')
    list_filter = ('menu_item',)
    search_fields = ('order__id', 'menu_item__name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'method', 'amount', 'is_paid', 'paid_at')
    list_filter = ('method', 'is_paid')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'menu_item', 'created_at')
    search_fields = ('user__username', 'user__email', 'menu_item__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'user', 'rating', 'is_published', 'created_at')
    list_filter = ('rating', 'is_published', 'created_at')
    search_fields = ('menu_item__name', 'user__username', 'text')
    fields = ('user', 'menu_item', 'rating', 'text', 'image', 'is_published')
