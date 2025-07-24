from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Permit

@shared_task
def expire_old_pending_permits():
  threshold_time = timezone.now() - timedelta(minutes=5)
  count = Permit.objects.filter(status='pending', created_at__lt=threshold_time).update(status='expired')
  print(f"[Task] Expired {count} permits.")