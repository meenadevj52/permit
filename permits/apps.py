from django.apps import AppConfig

class PermitsConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'permits'

  def ready(self):
    import permits.signals
    import permits.periodic_tasks
