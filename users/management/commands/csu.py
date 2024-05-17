from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания супер-пользователя (админа)"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.ru',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            )

        user.set_password('123qwerty456')
        user.save()
