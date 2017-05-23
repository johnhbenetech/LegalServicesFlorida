from django.apps import AppConfig


class ProviderConfig(AppConfig):
    name = 'provider'
    def ready(self):
        from . import signals