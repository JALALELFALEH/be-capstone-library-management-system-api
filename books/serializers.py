from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'published_date',
            'total_copies', 'available_copies', 'created_at', 'is_available'
        ]
        read_only_fields = ['created_at', 'available_copies']
    
    def validate_isbn(self, value):
        """Validate ISBN format (10 or 13 digits)"""
        if not value.isdigit() or len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits")
        return value
    
    def validate_total_copies(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total copies must be positive")
        return value