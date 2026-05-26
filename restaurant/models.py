from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(null = True,blank=True, verbose_name="Описание категории")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class MenuItem(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='menu_items')
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    composition = models.TextField(blank=True, verbose_name='Состав')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    weight_grams = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category__name', 'name']
        unique_together = ['category', 'name']

    def __str__(self):
        return self.name


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    photo = models.ImageField(upload_to='users/', blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.user}'


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        COOKING = 'cooking', 'Cooking'
        DELIVERY = 'delivery', 'Delivery'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,
        blank=True,
    )
    delivery_city = models.CharField(max_length=80, default='Moscow')
    delivery_street = models.CharField(max_length=160, blank=True)
    delivery_building = models.CharField(max_length=32, blank=True)
    delivery_apartment = models.CharField(max_length=32, blank=True)
    delivery_comment = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ['order', 'menu_item']

    def __str__(self):
        return f'{self.menu_item} x {self.quantity}'


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'
        ONLINE = 'online', 'Online'

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payment for order #{self.order_id}'


class Favorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['user', 'menu_item']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.menu_item}'


class Review(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f'Review for {self.menu_item}'
