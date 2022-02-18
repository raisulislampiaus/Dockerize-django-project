from django.apps import AppConfig


class PiausConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'piaus'
    
    def ready(self):
        import piaus.signals
