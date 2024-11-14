# schedules/apps.py
from django.apps import AppConfig

class SchedulesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Adds default auto field
    name = 'schedules'

    def ready(self):
        import schedules.signals  # Ensures signals are loaded
