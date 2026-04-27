import os

from django.contrib.auth import get_user_model


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add create superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.create(email="admin@mail.ru")
        user.set_password(os.getenv("CSU_PASSWORD"))
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
