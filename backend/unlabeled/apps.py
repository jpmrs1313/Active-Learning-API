from django.apps import AppConfig


class UnlabeledConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'unlabeled'
