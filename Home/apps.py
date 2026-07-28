from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'Home'

    def ready(self):
        import Home.signals  # noqa: F401 — registers post_save signals
