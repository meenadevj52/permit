from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Permit

@receiver(post_save, sender=Permit)
def handle_permit_creation(sender, instance, created, **kwargs):
  if created:
    print(f"[Signal] New permit created with ID: {instance.id}")
  else:
    print(f"[Signal] Permit updated with ID: {instance.id} and status: {instance.status}")