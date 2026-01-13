import requests
from .conf import paypal_settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class PayPalClient:
    """PayPal API client for handling payment operations"""
    
    def __init__(self):
        self.base_url = paypal_settings.BASE_URL
        self.client_id = paypal_settings.CLIENT_ID
        self.client_secret = paypal_settings.CLIENT_SECRET
    
    def get_access_token(self):
        """Get OAuth access token from PayPal"""
        cached_token = cache.get('paypal_access_token')
        if cached_token:
            return cached_token
        
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }
        data = {'grant_type': 'client_credentials'}
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=data,
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            token_data = response.json()
            access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600) - 60
            
            cache.set('paypal_access_token', access_token, expires_in)
            return access_token
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get PayPal access token: {e}")
            raise
    
    def create_order(self, amount, currency='USD', description='', return_url=None, cancel_url=None):
        """Create a PayPal order"""
        access_token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        
        return_url = return_url or paypal_settings.RETURN_URL
        cancel_url = cancel_url or paypal_settings.CANCEL_URL
        
        payload = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': currency,
                    'value': str(amount)
                },
                'description': description
            }],
            'application_context': {
                'return_url': return_url,
                'cancel_url': cancel_url,
                'brand_name': 'Your Brand',
                'user_action': 'PAY_NOW'
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create PayPal order: {e}")
            raise
    
    def capture_order(self, order_id):
        """Capture a PayPal order"""
        access_token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to capture PayPal order: {e}")
            raise
    
    def get_order(self, order_id):
        """Get order details"""
        access_token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders/{order_id}"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get PayPal order: {e}")
            raise
