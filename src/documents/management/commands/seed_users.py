"""
seed_users — creates default users that come pre-installed.

Each user is created only if no user with that username already exists,
so running this command multiple times is safe (idempotent).
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

DEFAULT_USERS = [
    {
        "username": "admin",
        "email": "admin@gmail.com",
        "password": "12345",
        "is_superuser": True,
        "is_staff": True,
    },
]


class Command(BaseCommand):
    help = "Creates default users if they do not already exist."

    def handle(self, *args, **options):
        for spec in DEFAULT_USERS:
            username = spec["username"]
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  User '{username}' already exists, skipping.")
                continue
            User.objects.create_superuser(
                username=username,
                email=spec["email"],
                password=spec["password"],
            )
            self.stdout.write(self.style.SUCCESS(f"  Created user '{username}'."))
