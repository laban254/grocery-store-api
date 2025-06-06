from django.urls import path

from .auth_views import GoogleCallbackView, GoogleLoginView
from .views import UserProfileView

urlpatterns = [
    # Single user profile endpoint that includes all user information
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("oauth/google/", GoogleLoginView.as_view(), name="api-google-login"),
    path("oauth/google/callback/", GoogleCallbackView.as_view(), name="api-google-callback"),
]
