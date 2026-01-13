# django-checkout-paypal

A Django package for integrating PayPal payments into your Django application.

## Features

- Easy PayPal integration for Django projects
- Support for PayPal Orders API v2
- Transaction tracking and management
- Django admin integration
- Sandbox and live mode support
- Secure OAuth2 authentication with token caching

## Installation

```bash
pip install django-paypal-checkout
```

## Quick Start

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'paypal',
]
```

### 2. Configure Settings

Add these settings to your `settings.py`:

```python
# PayPal Configuration
PAYPAL_CLIENT_ID = 'your-paypal-client-id'
PAYPAL_CLIENT_SECRET = 'your-paypal-client-secret'
PAYPAL_MODE = 'sandbox'  # Use 'live' for production

# Optional: Override default URLs
PAYPAL_RETURN_URL = 'https://yourdomain.com/payment/success/'
PAYPAL_CANCEL_URL = 'https://yourdomain.com/payment/cancel/'
```

### 3. Add URLs

Include the django-paypal-checkout URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('paypal/', include('paypal.urls')),
]
```

### 4. Run Migrations

```bash
python manage.py migrate paypal
```

## Usage

### Creating a Payment

You can create a payment in two ways:

#### Option 1: Using the built-in view

Create a form in your template:

```html
<form method="POST" action="{% url 'paypal:create_payment' %}">
    {% csrf_token %}
    <input type="hidden" name="amount" value="99.99">
    <input type="hidden" name="currency" value="USD">
    <input type="hidden" name="description" value="Product Purchase">
    <button type="submit">Pay with PayPal</button>
</form>
```

#### Option 2: Using the PayPalClient programmatically

```python
from paypal.client import PayPalClient
from paypal.models import PayPalTransaction

# Create transaction record
transaction = PayPalTransaction.objects.create(
    user=request.user,
    amount=99.99,
    currency='USD',
    description='Product Purchase'
)

# Create PayPal order
client = PayPalClient()
order = client.create_order(
    amount=99.99,
    currency='USD',
    description='Product Purchase',
    return_url='https://yourdomain.com/success/',
    cancel_url='https://yourdomain.com/cancel/'
)

# Save order ID to transaction
transaction.paypal_order_id = order['id']
transaction.save()

# Redirect user to PayPal
approval_url = next(link['href'] for link in order['links'] if link['rel'] == 'approve')
return redirect(approval_url)
```

### Handling Payment Results

Create views to handle success, failure, and cancellation:

```python
from django.views.generic import TemplateView

class PaymentSuccessView(TemplateView):
    template_name = 'payment_success.html'

class PaymentFailedView(TemplateView):
    template_name = 'payment_failed.html'

class PaymentCancelledView(TemplateView):
    template_name = 'payment_cancelled.html'
```

Add these to your urls.py:

```python
urlpatterns = [
    ...
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', PaymentFailedView.as_view(), name='payment_failed'),
    path('payment/cancelled/', PaymentCancelledView.as_view(), name='payment_cancelled'),
]
```

## Models

### PayPalTransaction

The main model for tracking PayPal transactions:

**Fields:**
- `id`: UUID primary key
- `user`: ForeignKey to User model
- `amount`: Transaction amount
- `currency`: Currency code (default: USD)
- `description`: Transaction description
- `paypal_order_id`: PayPal order ID
- `paypal_payment_id`: PayPal payment ID
- `payer_id`: Payer ID
- `payer_email`: Payer email
- `status`: Transaction status (pending, completed, failed, cancelled, refunded)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `completed_at`: Completion timestamp
- `metadata`: JSON field for additional data

**Methods:**
- `mark_completed()`: Mark transaction as completed
- `mark_failed()`: Mark transaction as failed
- `mark_cancelled()`: Mark transaction as cancelled

## API Client

### PayPalClient

The main client for interacting with PayPal API:

```python
from paypal.client import PayPalClient

client = PayPalClient()

# Create an order
order = client.create_order(
    amount=99.99,
    currency='USD',
    description='Product description'
)

# Capture an order
capture_data = client.capture_order(order_id='ORDER_ID')

# Get order details
order_details = client.get_order(order_id='ORDER_ID')
```

## Getting PayPal Credentials

1. Go to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. Log in with your PayPal account
3. Navigate to "Apps & Credentials"
4. Create a new app or use an existing one
5. Copy the Client ID and Secret
6. Use sandbox credentials for testing, live credentials for production

## Testing

The package uses PayPal's sandbox environment by default. To test:

1. Create a sandbox account at [PayPal Developer](https://developer.paypal.com/)
2. Use sandbox credentials in your settings
3. Use sandbox buyer accounts for testing payments

## Security Notes

- Never commit your PayPal credentials to version control
- Use environment variables for sensitive settings
- Always use HTTPS in production
- Validate transaction amounts server-side

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.

## Changelog

### Version 0.1.0
- Initial release
- PayPal Orders API v2 integration
- Transaction tracking
- Django admin integration
- Sandbox and live mode support