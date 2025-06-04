from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        try:
            # Import and register signals
            from accounts import signals  # noqa
        except ImportError:
            pass
