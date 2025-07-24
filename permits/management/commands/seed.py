from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
  help = "Seed the database with one admin user"

  def handle(self, *args, **kwargs):
    admin_username = 'admin_user'
    admin_password = 'Admin@123'

    if not User.objects.filter(username=admin_username).exists():
      User.objects.create_user(
        username=admin_username,
        password=admin_password,
        role='admin'
      )
      self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin_username}"))
    else:
      self.stdout.write(self.style.WARNING("Admin user already exists"))
