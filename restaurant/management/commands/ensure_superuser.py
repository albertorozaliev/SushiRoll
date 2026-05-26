import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a Django superuser from environment variables if it does not exist.'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@sushiroll.local')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin12345')

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )

        if created:
            user.set_password(password)
            user.save(update_fields=['password'])
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
            return

        updated_fields = []
        if not user.is_staff:
            user.is_staff = True
            updated_fields.append('is_staff')
        if not user.is_superuser:
            user.is_superuser = True
            updated_fields.append('is_superuser')
        if email and user.email != email:
            user.email = email
            updated_fields.append('email')

        if updated_fields:
            user.save(update_fields=updated_fields)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" updated.'))
            return

        self.stdout.write(f'Superuser "{username}" already exists.')
