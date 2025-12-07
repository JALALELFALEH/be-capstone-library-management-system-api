from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/books/', include('books.urls')),
    path('api/users/', include('users.urls')),
    path('api/transactions/', include('transactions.urls')),
    
    # DRF browsable API auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)