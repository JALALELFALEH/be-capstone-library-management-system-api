"""
Main serverless function for Vercel
This acts as a WSGI gateway for Django
"""
import sys
import os

# Add your project to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')

# Import Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel handler
def handler(request, response):
    """Vercel serverless function handler"""
    from django.http import HttpRequest, HttpResponse
    from django.core.handlers.wsgi import WSGIHandler
    
    # Convert Vercel request to Django request
    django_request = HttpRequest()
    django_request.method = request['method']
    django_request.path = request['path']
    django_request.META = request['headers']
    
    # Get Django response
    wsgi_handler = WSGIHandler()
    django_response = wsgi_handler(django_request)
    
    # Convert to Vercel response
    response['statusCode'] = django_response.status_code
    response['headers'] = dict(django_response.items())
    response['body'] = django_response.content.decode('utf-8')
    
    return response