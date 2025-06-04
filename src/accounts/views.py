from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .schemas import get_user_profile_schema, oidc_token_schema, update_user_profile_schema
from .serializers import UserSerializer, UserUpdateSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a user's profile.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UserUpdateSerializer

    def get_object(self):
        """
        Get the authenticated user object.
        """
        return self.request.user

    @extend_schema(**get_user_profile_schema)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(**update_user_profile_schema)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(**update_user_profile_schema)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update the user's profile.
        """
        # Don't allow changing the email
        if "email" in request.data:
            del request.data["email"]

        return super().update(request, *args, **kwargs)


class UserInfoView(APIView):
    """
    View for retrieving user information from OpenID Connect.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(**get_user_profile_schema)
    def get(self, request, *args, **kwargs):
        """
        Get user information including any OIDC-specific data.
        """
        user = request.user
        user_data = UserSerializer(user).data

        # Add OIDC specific information if available
        if hasattr(user, "oidc_id"):
            user_data["oidc_id"] = user.oidc_id
        if hasattr(user, "oidc_provider"):
            user_data["oidc_provider"] = user.oidc_provider

        # Get any social accounts
        social_accounts = []
        if hasattr(user, "socialaccount_set"):
            for account in user.socialaccount_set.all():
                social_accounts.append(
                    {
                        "provider": account.provider,
                        "uid": account.uid,
                        "last_login": account.last_login,
                        "date_joined": account.date_joined,
                    }
                )

        user_data["social_accounts"] = social_accounts

        return Response(user_data)


class OIDCTokenView(APIView):
    """
    View for exchanging an OIDC token for a JWT token.
    This is used after successful OIDC authentication to get a JWT token for API access.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(**oidc_token_schema)
    def post(self, request, *args, **kwargs):
        """
        Generate JWT tokens for the authenticated user.
        """
        user = request.user
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
