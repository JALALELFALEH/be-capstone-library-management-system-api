from django.urls import path
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserLogoutView, 
    UserProfileView,
    UserTransactionsView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/transactions/', UserTransactionsView.as_view(), name='user-transactions'),
]