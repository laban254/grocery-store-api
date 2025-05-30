from django.urls import path
from .views import UserProfileView, UserInfoView, OIDCTokenView
from .auth_views import (
    GoogleLoginView, OAuthProvidersView,
    GoogleCallbackView
)

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('oidc-token/', OIDCTokenView.as_view(), name='oidc-token'),
    
    # OAuth API endpoints for Swagger documentation
    path('oauth/providers/', OAuthProvidersView.as_view(), name='api-oauth-providers'),
    path('oauth/google/', GoogleLoginView.as_view(), name='api-google-login'),
    
    # OAuth callback endpoints
    path('oauth/google/callback/', GoogleCallbackView.as_view(), name='api-google-callback'),
]
