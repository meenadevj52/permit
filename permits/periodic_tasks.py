from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

@receiver(post_migrate)
def create_periodic_tasks(sender, **kwargs):
  if sender.name != 'permits':
    return

  schedule, _ = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES,
  )

  PeriodicTask.objects.get_or_create(
    interval=schedule,
    name='Expire old pending permits',
    task='permits.tasks.expire_old_pending_permits',
    defaults={'args': json.dumps([])},
  )
