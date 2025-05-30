from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlencode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, login
from allauth.socialaccount.models import SocialApp, SocialLogin, SocialToken, SocialAccount
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
        redirect_uri = request.build_absolute_uri(reverse(f'api-{self.provider_name}-callback'))
        
        # Get authorization URL and parameters from the adapter
        if hasattr(self.oauth2_adapter, 'authorize_url'):
            authorization_url = self.oauth2_adapter.authorize_url
        else:
            # Google uses accounts.google.com/o/oauth2/auth
            if self.provider_name == 'google':
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
    
    This endpoint initiates the Google OAuth authentication flow by redirecting
    the user to Google's authorization page. After successful authentication,
    Google will redirect back to the callback URL with an authorization code.
    """
    provider_name = 'google'
    oauth2_adapter = GoogleOAuth2Adapter
    
    @extend_schema(
        description="""
        Initiates Google OAuth login flow.
        
        Redirects the user to Google's authorization page. After authentication,
        Google will redirect back to the callback URL with an authorization code.
        
        No parameters are required for this endpoint.
        """,
        responses={
            302: OpenApiResponse(description="Redirects to Google's authorization page"),
        },
        tags=["Authentication"],
        operation_id="google_oauth_login"
    )
    def get(self, request):
        return super().get(request)


class OAuthProvidersView(APIView):
    """
    View that lists all available OAuth providers.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        description="""
        Returns a list of available OAuth/OpenID Connect providers for authentication.
        
        This endpoint provides information about the available authentication providers,
        including their names, login URLs, and descriptions. Use these URLs to initiate
        the authentication flow with the respective providers.
        
        Available providers:
        - Google (OpenID Connect compliant)
        - Generic OpenID Connect
        """,
        responses={
            200: OpenApiResponse(
                description="List of available OAuth providers",
                examples=[
                    OpenApiExample(
                        name="providers_example",
                        value={
                            "providers": [
                                {
                                    "name": "Google",
                                    "login_url": "/api/accounts/oauth/google/",
                                    "description": "Login with your Google account"
                                },
                                {
                                    "name": "OpenID Connect",
                                    "login_url": "/accounts/openid_connect/login/",
                                    "description": "Login with your OpenID Connect provider"
                                }
                            ],
                            "note": "These URLs will redirect to the respective OAuth provider's login page."
                        }
                    )
                ]
            )
        },
        tags=["Authentication"],
        operation_id="list_oauth_providers"
    )
    def get(self, request):
        """
        Returns a list of available OAuth providers.
        """
        providers = [
            {
                "name": "Google",
                "login_url": request.build_absolute_uri(reverse('api-google-login')),
                "description": "Login with your Google account"
            },
            {
                "name": "OpenID Connect",
                "login_url": request.build_absolute_uri('/accounts/openid_connect/login/'),
                "description": "Login with your OpenID Connect provider"
            }
        ]
        
        return Response({
            "providers": providers,
            "note": "These URLs will redirect to the respective OAuth provider's login page."
        })


class OAuthCallbackView(APIView):
    """
    Base view for handling OAuth callbacks and generating JWT tokens.
    """
    permission_classes = [AllowAny]
    provider_name = None
    oauth2_adapter = None

    @extend_schema(
        description="""
        Handles the OAuth callback from the provider and returns JWT tokens.
        
        **Note:** This endpoint is part of the OAuth flow and is called automatically after a user authenticates with an OAuth provider. 
        The `code` parameter is provided by the OAuth provider when redirecting back to your application.
        The `state` parameter is used for CSRF protection if provided in the initial authorization request.
        """,
        parameters=[
            OpenApiParameter(name="code", description="Authorization code from OAuth provider", required=True, type=str),
            OpenApiParameter(name="state", description="State parameter for CSRF protection", required=False, type=str),
        ],
        responses={
            200: OpenApiResponse(description="JWT tokens generated successfully"),
            400: OpenApiResponse(description="Error in OAuth callback process"),
        },
        tags=["Authentication"]
    )
    def get(self, request):
        """
        Handles the OAuth callback from the provider and returns JWT tokens.
        """
        code = request.GET.get('code')
        if not code:
            return Response({"error": "No authorization code provided"}, status=400)
        
        # Get client credentials from settings
        client_id = settings.SOCIALACCOUNT_PROVIDERS.get(self.provider_name, {}).get('APP', {}).get('client_id')
        client_secret = settings.SOCIALACCOUNT_PROVIDERS.get(self.provider_name, {}).get('APP', {}).get('secret')
        
        if not client_id or not client_secret:
            return Response({"error": f"No client credentials configured for {self.provider_name}"}, status=400)
        
        # Build the redirect URI (must match the one used in the authorization request)
        redirect_uri = request.build_absolute_uri(reverse(f'api-{self.provider_name}-callback'))
        
        # Exchange the authorization code for an access token
        token_url = self.get_token_url()
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        
        token_response = requests.post(token_url, data=token_data)
        if token_response.status_code != 200:
            return Response({"error": f"Failed to obtain access token: {token_response.text}"}, status=400)
        
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        
        if not access_token:
            return Response({"error": "No access token in provider response"}, status=400)
        
        # Fetch user info from the provider's API
        user_info = self.get_user_info(access_token)
        if not user_info:
            return Response({"error": "Failed to obtain user information"}, status=400)
        
        # Find or create user
        email = user_info.get('email')
        if not email:
            return Response({"error": "No email found in user information"}, status=400)
        
        # Get or create user with OIDC information
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': user_info.get('login') or user_info.get('name', '').replace(' ', '_').lower(),
                'is_active': True,
                'oidc_id': user_info.get('id'),
                'oidc_provider': self.provider_name,
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
            }
        )
        
        # Update OIDC info for existing users as well
        if not created:
            user.oidc_id = user_info.get('id')
            user.oidc_provider = self.provider_name
            if user_info.get('given_name') and not user.first_name:
                user.first_name = user_info.get('given_name')
            if user_info.get('family_name') and not user.last_name:
                user.last_name = user_info.get('family_name')
            user.save()
        
        # Get phone number if available
        phone_number = None
        if token_json.get('access_token'):  # Only try if we have a token
            try:
                phone_response = requests.get(
                    'https://people.googleapis.com/v1/people/me',
                    params={'personFields': 'phoneNumbers'},
                    headers={'Authorization': f'Bearer {token_json["access_token"]}'}
                )
                if phone_response.status_code == 200:
                    phone_data = phone_response.json()
                    phone_numbers = phone_data.get('phoneNumbers', [])
                    if phone_numbers:
                        phone_number = phone_numbers[0].get('value')
            except Exception as e:
                # Log the error but continue without phone number
                print(f"Error fetching phone number: {e}")
        
        # Update user phone if available
        if phone_number and not user.phone:
            user.phone = phone_number
            user.save()
            
        # Create or update social account
        social_account, _ = SocialAccount.objects.get_or_create(
            provider=self.provider_name,
            uid=str(user_info.get('id')),
            defaults={'user': user}
        )
        
        if social_account.user != user:
            social_account.user = user
            social_account.save()
        
        # Log the user in with a specific backend
        from django.contrib.auth import get_backends
        backend = get_backends()[0]  # Use the first configured backend
        login(request, user, backend=backend.__class__.__module__ + '.' + backend.__class__.__name__)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
            }
        })
    
    def get_token_url(self):
        """Get the token URL for the provider."""
        if self.provider_name == 'google':
            return 'https://oauth2.googleapis.com/token'
        return None
    
    def get_user_info(self, access_token):
        """Get user info from the provider API."""
        if self.provider_name == 'google':
            headers = {'Authorization': f'Bearer {access_token}'}
            user_response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
            if user_response.status_code != 200:
                return None
            return user_response.json()
            
        return None


class GoogleCallbackView(OAuthCallbackView):
    """
    Handles Google OAuth callback and generates JWT tokens.
    
    This endpoint is called by Google after successful authentication. It exchanges
    the authorization code for an access token, retrieves user information, and 
    creates or updates the user account accordingly. Finally, it returns JWT tokens
    for API authentication.
    """
    provider_name = 'google'
    oauth2_adapter = GoogleOAuth2Adapter
    
    @extend_schema(
        description="""
        Google OAuth callback endpoint.
        
        This endpoint receives the authorization code from Google after successful authentication.
        It exchanges the code for an access token, retrieves the user's information from Google,
        and returns JWT tokens for API authentication.
        
        **Parameters:**
        - `code`: The authorization code provided by Google
        - `state`: Optional state parameter for CSRF protection
        
        **Returns:**
        - JWT access and refresh tokens
        - Basic user information
        """,
        parameters=[
            OpenApiParameter(name="code", description="Authorization code from Google", required=True, type=str),
            OpenApiParameter(name="state", description="State parameter for CSRF protection", required=False, type=str),
        ],
        responses={
            200: OpenApiResponse(description="JWT tokens generated successfully"),
            400: OpenApiResponse(description="Error in OAuth callback process"),
        },
        tags=["Authentication"],
        operation_id="google_oauth_callback"
    )
    def get(self, request):
        return super().get(request)
