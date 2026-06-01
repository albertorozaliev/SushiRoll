from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import Category, MenuItem

User = get_user_model()


class MenuItemListViewTests(TestCase):
    def test_active_categories_are_loaded_from_database(self):
        Category.objects.create(name='Роллы')
        Category.objects.create(name='Пицца')

        response = self.client.get(reverse('products'))

        self.assertContains(response, 'Роллы')
        self.assertContains(response, 'Пицца')
        self.assertContains(response, '?category=picca')

    def test_menu_items_can_be_filtered_by_new_category_slug(self):
        rolls = Category.objects.create(name='Роллы')
        pizza = Category.objects.create(name='Пицца')
        MenuItem.objects.create(category=rolls, name='Филадельфия', price=500)
        MenuItem.objects.create(category=pizza, name='Маргарита', price=650)

        response = self.client.get(reverse('products'), {'category': 'picca'})

        self.assertContains(response, 'Маргарита')
        self.assertNotContains(response, 'Филадельфия')

    def test_slug_is_generated_from_russian_name(self):
        category = Category.objects.create(name='Горячие роллы')
        menu_item = MenuItem.objects.create(category=category, name='Филадельфия люкс', price=700)

        self.assertEqual(category.slug, 'goryachie-rolly')
        self.assertEqual(menu_item.slug, 'filadelfiya-lyuks')


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='client', password='pass12345')
        self.staff = User.objects.create_user(username='manager', password='pass12345', is_staff=True)

    def test_api_requires_authentication(self):
        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_read_with_search_and_page_size(self):
        Category.objects.create(name='Роллы')
        Category.objects.create(name='Пицца')
        self.client.force_authenticate(self.user)

        response = self.client.get('/api/categories/', {'search': 'Пицца', 'page_size': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Пицца')

    def test_authenticated_user_cannot_create(self):
        self.client.force_authenticate(self.user)

        response = self.client.post('/api/categories/', {'name': 'Сеты'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_update_and_delete(self):
        self.client.force_authenticate(self.staff)

        create_response = self.client.post('/api/categories/', {'name': 'Сеты'}, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        category_id = create_response.data['id']
        self.assertEqual(create_response.data['slug'], 'sety')

        update_response = self.client.patch(
            f'/api/categories/{category_id}/',
            {'description': 'Комбо-наборы'},
            format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['description'], 'Комбо-наборы')

        delete_response = self.client.delete(f'/api/categories/{category_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class AuthViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client', password='pass12345')
        self.staff = User.objects.create_user(username='manager', password='pass12345', is_staff=True)

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password1': 'StrongPass12345',
            'password2': 'StrongPass12345',
        })

        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_shows_login_links_for_guest(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Войти')
        self.assertContains(response, 'Регистрация')

    def test_login_shows_user_profile(self):
        self.client.login(username='client', password='pass12345')

        response = self.client.get(reverse('profile'))

        self.assertContains(response, 'client')
        self.assertContains(response, 'пользователь')

    def test_data_link_is_visible_only_for_staff(self):
        self.client.login(username='client', password='pass12345')
        user_response = self.client.get(reverse('information'))
        self.assertNotContains(user_response, 'Данные')

        self.client.logout()
        self.client.login(username='manager', password='pass12345')
        staff_response = self.client.get(reverse('information'))
        self.assertContains(staff_response, 'Данные')

    def test_regular_user_cannot_open_data_section(self):
        self.client.login(username='client', password='pass12345')

        response = self.client.get(reverse('data_index'))

        self.assertEqual(response.status_code, 403)
