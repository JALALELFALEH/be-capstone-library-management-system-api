from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from django.db import transaction as db_transaction
from .models import Transaction
from .serializers import TransactionSerializer, CheckoutSerializer
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Transaction operations (ReadOnly)"""
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users see their own transactions, admins see all"""
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all().order_by('-transaction_date')
        return Transaction.objects.filter(user=user).order_by('-transaction_date')
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Checkout a book"""
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            
            try:
                with db_transaction.atomic():
                    book = Book.objects.select_for_update().get(id=book_id)
                    
                    # Check if book is available
                    if book.available_copies <= 0:
                        return Response(
                            {'error': 'Book not available'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Check if user already has this book checked out
                    existing_checkout = Transaction.objects.filter(
                        user=request.user,
                        book=book,
                        transaction_type='CHECKOUT',
                        returned_date__isnull=True
                    ).exists()
                    
                    if existing_checkout:
                        return Response(
                            {'error': 'You already have this book checked out'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Create checkout transaction
                    checkout = Transaction.objects.create(
                        user=request.user,
                        book=book,
                        transaction_type='CHECKOUT'
                    )
                    
                    # Update book available copies
                    book.available_copies -= 1
                    book.save()
                    
                    return Response(
                        TransactionSerializer(checkout).data,
                        status=status.HTTP_201_CREATED
                    )
                    
            except Book.DoesNotExist:
                return Response(
                    {'error': 'Book not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return a checked out book"""
        try:
            transaction = Transaction.objects.get(id=pk)
            
            # Check permissions
            if not (request.user.is_staff or transaction.user == request.user):
                return Response(
                    {'error': 'You do not have permission to return this book'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if already returned
            if transaction.returned_date is not None:
                return Response(
                    {'error': 'Book already returned'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with db_transaction.atomic():
                # Update transaction
                transaction.returned_date = timezone.now()
                transaction.transaction_type = 'RETURN'
                transaction.save()
                
                # Update book available copies
                book = transaction.book
                book.available_copies += 1
                book.save()
                
                return Response(
                    TransactionSerializer(transaction).data,
                    status=status.HTTP_200_OK
                )
                
        except Transaction.DoesNotExist:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue books (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        overdue_transactions = Transaction.objects.filter(
            transaction_type='CHECKOUT',
            returned_date__isnull=True,
            due_date__lt=timezone.now()
        )
        
        serializer = self.get_serializer(overdue_transactions, many=True)
        return Response(serializer.data)