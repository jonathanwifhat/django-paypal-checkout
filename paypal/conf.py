from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class PayPalSettings:
    """PayPal configuration settings"""
    
    @property
    def CLIENT_ID(self):
        client_id = getattr(settings, 'PAYPAL_CLIENT_ID', None)
        if not client_id:
            raise ImproperlyConfigured('PAYPAL_CLIENT_ID must be set in settings')
        return client_id
    
    @property
    def CLIENT_SECRET(self):
        secret = getattr(settings, 'PAYPAL_CLIENT_SECRET', None)
        if not secret:
            raise ImproperlyConfigured('PAYPAL_CLIENT_SECRET must be set in settings')
        return secret
    
    @property
    def MODE(self):
        return getattr(settings, 'PAYPAL_MODE', 'sandbox')
    
    @property
    def BASE_URL(self):
        if self.MODE == 'live':
            return 'https://api-m.paypal.com'
        return 'https://api-m.sandbox.paypal.com'
    
    @property
    def RETURN_URL(self):
        return getattr(settings, 'PAYPAL_RETURN_URL', '/paypal/success/')
    
    @property
    def CANCEL_URL(self):
        return getattr(settings, 'PAYPAL_CANCEL_URL', '/paypal/cancel/')

paypal_settings = PayPalSettings()