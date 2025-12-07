from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book CRUD operations"""
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'isbn']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'author', 'published_date', 'created_at']
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get only available books"""
        available_books = Book.objects.filter(available_copies__gt=0)
        
        # Apply filters
        author = request.query_params.get('author', None)
        if author:
            available_books = available_books.filter(author__icontains=author)
        
        search = request.query_params.get('search', None)
        if search:
            available_books = available_books.filter(
                title__icontains=search
            ) | available_books.filter(
                author__icontains=search
            ) | available_books.filter(
                isbn__icontains=search
            )
        
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Set available copies equal to total copies for new books"""
        total_copies = serializer.validated_data.get('total_copies', 1)
        serializer.save(available_copies=total_copies)