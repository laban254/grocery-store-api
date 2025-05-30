from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlencode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import requests
import json

User = get_user_model()

class OAuthLoginView(APIView):
    """
    Base view for OAuth login redirection.
    """
    permission_classes = [AllowAny]
    provider_name = None
    oauth2_adapter = None

    @extend_schema(
        description="Redirects directly to the OAuth provider's authorization page.",
        responses={
            302: OpenApiResponse(description="Redirects to the OAuth provider's authorization page"),
        },
        tags=["Authentication"]
    )
    def get(self, request):
        """
        Redirects directly to the OAuth provider's authorization page.
        """
        if self.oauth2_adapter is None:
            return HttpResponseRedirect(reverse(f'{self.provider_name}_login'))
            
        # Get the client ID from settings
        client_id = settings.SOCIALACCOUNT_PROVIDERS.get(self.provider_name, {}).get('APP', {}).get('client_id')
        if not client_id:
            return Response({"error": f"No client ID configured for {self.provider_name}"}, status=400)
        
        # Build the redirect URI
        redirect_uri = request.build_absolute_uri(f'/accounts/{self.provider_name}/login/callback/')
        
        # Get authorization URL and parameters from the adapter
        if hasattr(self.oauth2_adapter, 'authorize_url'):
            authorization_url = self.oauth2_adapter.authorize_url
        else:
            # GitHub uses github.com/login/oauth/authorize
            if self.provider_name == 'github':
                authorization_url = 'https://github.com/login/oauth/authorize'
            # Google uses accounts.google.com/o/oauth2/auth
            elif self.provider_name == 'google':
                authorization_url = 'https://accounts.google.com/o/oauth2/auth'
            else:
                return Response({"error": f"No authorization URL for {self.provider_name}"}, status=400)
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(settings.SOCIALACCOUNT_PROVIDERS.get(self.provider_name, {}).get('SCOPE', [])),
        }
        
        # Construct the full authorization URL with parameters
        full_url = f"{authorization_url}?{urlencode(params)}"
        return HttpResponseRedirect(full_url)


class GoogleLoginView(OAuthLoginView):
    """
    Redirects directly to Google OAuth login.
    """
    provider_name = 'google'
    oauth2_adapter = GoogleOAuth2Adapter
    

class GitHubLoginView(OAuthLoginView):
    """
    Redirects directly to GitHub OAuth login.
    """
    provider_name = 'github'
    oauth2_adapter = GitHubOAuth2Adapter


class OAuthProvidersView(APIView):
    """
    View that lists all available OAuth providers.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        description="Returns a list of available OAuth providers for authentication.",
        responses={
            200: OpenApiResponse(description="List of available OAuth providers"),
        },
        tags=["Authentication"]
    )
    def get(self, request):
        """
        Returns a list of available OAuth providers.
        """
        providers = [
            {
                "name": "GitHub",
                "login_url": request.build_absolute_uri(reverse('api-github-login')),
                "description": "Login with your GitHub account"
            },
            {
                "name": "Google",
                "login_url": request.build_absolute_uri(reverse('api-google-login')),
                "description": "Login with your Google account"
            }
        ]
        
        return Response({
            "providers": providers,
            "note": "These URLs will redirect to the respective OAuth provider's login page."
        })
