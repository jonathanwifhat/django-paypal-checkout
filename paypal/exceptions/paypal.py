"""Custom exceptions for django-paypal-checkout integration."""

class PayPalException(Exception):
    """Base exception for PayPal errors"""
    pass

class PayPalAuthenticationError(PayPalException):
    """Raised when authentication with PayPal fails"""
    pass

class PayPalOrderCreationError(PayPalException):
    """Raised when order creation fails"""
    pass

class PayPalCaptureError(PayPalException):
    """Raised when order capture fails"""
    pass

class PayPalConfigurationError(PayPalException):
    """Raised when PayPal configuration is invalid"""
    pass