from django.db import models
from django.conf import settings
from django.utils import timezone
from books.models import Book

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('CHECKOUT', 'Checkout'),
        ('RETURN', 'Return'),
    ]
    
    # Use settings.AUTH_USER_MODEL instead of direct import
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.transaction_type == 'CHECKOUT' and not self.due_date:
            self.due_date = timezone.now() + timezone.timedelta(days=14)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.email} - {self.book.title}"