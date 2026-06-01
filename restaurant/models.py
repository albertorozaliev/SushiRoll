from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


TRANSLITERATION_MAP = str.maketrans({
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
})


def make_slug(value):
    transliterated = value.lower().translate(TRANSLITERATION_MAP)
    return slugify(transliterated) or 'item'


def make_unique_slug(instance, value):
    base_slug = make_slug(value)
    slug = base_slug
    index = 2
    queryset = instance.__class__.objects.filter(slug=slug)

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.exists():
        slug = f'{base_slug}-{index}'
        queryset = instance.__class__.objects.filter(slug=slug)
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
        index += 1

    return slug


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=140, unique=True, blank=True, verbose_name='Слаг категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание категории')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_unique_slug(self, self.name)
        super().save(*args, **kwargs)


class MenuItem(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='menu_items',
        verbose_name='Категория',
    )
    name = models.CharField(max_length=160, verbose_name='Название блюда')
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name='Слаг блюда')
    composition = models.TextField(blank=True, verbose_name='Состав')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена',
    )
    weight_grams = models.PositiveIntegerField(null=True, blank=True, verbose_name='Вес в граммах')
    is_available = models.BooleanField(default=True, verbose_name='Доступно')

    class Meta:
        ordering = ['category__name', 'name']
        unique_together = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_unique_slug(self, self.name)
        super().save(*args, **kwargs)


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    photo = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Фото')

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
        verbose_name='Пользователь',
    )
    delivery_city = models.CharField(max_length=80, default='Moscow', verbose_name='Город доставки')
    delivery_street = models.CharField(max_length=160, blank=True, verbose_name='Улица доставки')
    delivery_building = models.CharField(max_length=32, blank=True, verbose_name='Дом')
    delivery_apartment = models.CharField(max_length=32, blank=True, verbose_name='Квартира')
    delivery_comment = models.CharField(max_length=255, blank=True, verbose_name='Комментарий к доставке')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус заказа',
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Блюдо',
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Количество')
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена за единицу',
    )

    class Meta:
        unique_together = ['order', 'menu_item']

    def __str__(self):
        return f'{self.menu_item} x {self.quantity}'


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'
        ONLINE = 'online', 'Online'

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name='Заказ')
    method = models.CharField(max_length=20, choices=Method.choices, verbose_name='Способ оплаты')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Сумма оплаты',
    )
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')

    def __str__(self):
        return f'Payment for order #{self.order_id}'


class Favorite(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Блюдо',
    )

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
        verbose_name='Пользователь',
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='reviews', verbose_name='Блюдо')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Оценка')
    text = models.TextField(blank=True, verbose_name='Текст отзыва')
    image = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    def __str__(self):
        return f'Review for {self.menu_item}'
