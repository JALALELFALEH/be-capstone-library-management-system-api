from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'transaction_type', 'transaction_date', 'due_date', 'returned_date')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('user__email', 'book__title')
    readonly_fields = ('transaction_date',)
    date_hierarchy = 'transaction_date'