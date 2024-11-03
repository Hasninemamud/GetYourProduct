from django.apps import AppConfig


# class ProductsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'products'
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_app_config = 'products.apps.ProductsConfig'

    name = 'products'

    def ready(self):
        import products.signals
