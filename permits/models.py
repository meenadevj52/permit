from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  ROLE_CHOICES = (
      ('citizen', 'Citizen'),
      ('admin', 'Admin'),
  )
  role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='citizen')

class Permit(models.Model):
  STATUS_CHOICES = (
      ('pending', 'Pending'),
      ('approved', 'Approved'),
      ('revoked', 'Revoked'),
      ('expired', 'Expired'),
  )

  user = models.ForeignKey('User', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  license_plate = models.CharField(max_length=20)
  address = models.TextField()
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  revocation_reason = models.TextField(null=True, blank=True)