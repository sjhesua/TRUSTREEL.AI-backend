from django.apps import AppConfig


class VideomanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoManager'

    def ready(self):
        import videoManager.signals