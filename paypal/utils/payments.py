from decimal import Decimal
from typing import Optional

def format_amount(amount: float) -> str:
    """Format amount to 2 decimal places for PayPal"""
    return f"{Decimal(str(amount)):.2f}"

def validate_currency(currency: str) -> bool:
    """Validate currency code"""
    valid_currencies = [
        'AUD', 'BRL', 'CAD', 'CNY', 'CZK', 'DKK', 'EUR', 'HKD',
        'HUF', 'ILS', 'JPY', 'MYR', 'MXN', 'TWD', 'NZD', 'NOK',
        'PHP', 'PLN', 'GBP', 'RUB', 'SGD', 'SEK', 'CHF', 'THB', 'USD'
    ]
    return currency.upper() in valid_currencies

def get_approval_url(order_data: dict) -> Optional[str]:
    """Extract approval URL from PayPal order response"""
    if 'links' in order_data:
        for link in order_data['links']:
            if link.get('rel') == 'approve':
                return link.get('href')
    return None