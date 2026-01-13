from django.apps import AppConfig

class DjangoPaypalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paypal'
    verbose_name = 'Django PayPal Checkout'