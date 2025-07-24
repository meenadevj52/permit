from django.apps import AppConfig

class PermitsConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'permits'

  def ready(self):
    import permits.signals
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    import json

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Expire old pending permits',
        task='permits.tasks.expire_old_pending_permits',
        defaults={'args': json.dumps([])},
    )