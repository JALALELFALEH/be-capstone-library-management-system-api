from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LibraryUser

@admin.register(LibraryUser)
class LibraryUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_of_membership', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_of_membership')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'date_of_membership')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )