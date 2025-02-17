from django.apps import AppConfig


class MhcappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mhcapp"

    def ready(self):
        import mhcapp.signals  # Import the signals
