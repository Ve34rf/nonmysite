from django.apps import AppConfig


class TestRestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_rest'
    verbose_name = 'Блог'