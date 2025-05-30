from django.urls import path
from .views import CustomerProfileView, UserInfoView, OIDCTokenView
from .auth_views import GitHubLoginView, GoogleLoginView, OAuthProvidersView

urlpatterns = [
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('oidc-token/', OIDCTokenView.as_view(), name='oidc-token'),
    
    # OAuth API endpoints for Swagger documentation
    path('oauth/providers/', OAuthProvidersView.as_view(), name='api-oauth-providers'),
    path('oauth/github/', GitHubLoginView.as_view(), name='api-github-login'),
    path('oauth/google/', GoogleLoginView.as_view(), name='api-google-login'),
]
