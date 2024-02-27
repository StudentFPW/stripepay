import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            print("Creating account for admin")
            admin = User.objects.create_superuser(
                email=os.getenv("ADMIN_EMAIL"),
                username=os.getenv("ADMIN_USERNAME"),
                password=os.getenv("ADMIN_PASSWORD"),
            )
            admin.is_active = True
            admin.is_staff = True
            admin.is_admin = True
            admin.save()
            print("Account created")
        else:
            print("Admin accounts can only be initialized if no Accounts exist")
