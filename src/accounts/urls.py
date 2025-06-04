from django.urls import path
from .views import UserProfileView
from .auth_views import (
    GoogleLoginView, GoogleCallbackView
)

urlpatterns = [
    # Single user profile endpoint that includes all user information
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # OAuth endpoints (only the essential ones)
    path('oauth/google/', GoogleLoginView.as_view(), name='api-google-login'),
    path('oauth/google/callback/', GoogleCallbackView.as_view(), name='api-google-callback'),
]
