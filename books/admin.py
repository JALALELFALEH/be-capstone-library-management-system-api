from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available_copies', 'total_copies', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Book Details', {
            'fields': ('title', 'author', 'isbn', 'published_date')
        }),
        ('Inventory', {
            'fields': ('total_copies', 'available_copies')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )