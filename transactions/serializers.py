from rest_framework import serializers
from .models import Transaction
from books.models import Book
from books.serializers import BookSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'user_email', 'book', 'book_details', 
            'transaction_type', 'transaction_date', 'due_date', 
            'returned_date', 'is_overdue'
        ]
        read_only_fields = ['user', 'transaction_date', 'due_date', 'returned_date']
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()

class CheckoutSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    
    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
            if not book.is_available():
                raise serializers.ValidationError("Book is not available")
            return value
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")

class ReturnSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()