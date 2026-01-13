from django.contrib import admin
from .models import PayPalTransaction

@admin.register(PayPalTransaction)
class PayPalTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['user__email', 'paypal_order_id', 'paypal_payment_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Transaction Info', {
            'fields': ('id', 'user', 'amount', 'currency', 'description', 'status')
        }),
        ('PayPal Details', {
            'fields': ('paypal_order_id', 'paypal_payment_id', 'payer_id', 'payer_email')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )