from drf_spectacular.utils import OpenApiExample
from rest_framework import status


# Helper functions to make response schemas more concise
def create_success_example(title, data, message, status_code):
    """Create a standardized success response example for API documentation"""
    return {
        "schema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "example": "success"},
                "message": {"type": "string", "example": message},
                "status_code": {"type": "integer", "example": status_code},
                "data": {"type": "object", "example": data},
            },
        },
        "examples": [
            {
                "name": title,
                "value": {
                    "status": "success",
                    "message": message,
                    "status_code": status_code,
                    "data": data,
                },
            }
        ],
    }


def get_standard_responses(include=None, validation_type=None):
    """Create standardized error responses for API documentation"""
    responses = {
        status.HTTP_400_BAD_REQUEST: {
            "schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "error"},
                    "message": {"type": "string", "example": "Validation error"},
                    "status_code": {"type": "integer", "example": 400},
                    "errors": {
                        "type": "object",
                        "example": {"field": ["Error message"]},
                    },
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "error"},
                    "message": {"type": "string", "example": "Authentication required"},
                    "status_code": {"type": "integer", "example": 401},
                },
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "error"},
                    "message": {"type": "string", "example": "Permission denied"},
                    "status_code": {"type": "integer", "example": 403},
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "error"},
                    "message": {"type": "string", "example": "Resource not found"},
                    "status_code": {"type": "integer", "example": 404},
                },
            }
        },
    }

    if include:
        return {k: v for k, v in responses.items() if k in include}
    return responses


# Schema for retrieving user profile
get_user_profile_schema = {
    "summary": "Get User Profile",
    "description": "Retrieve the profile information for the authenticated user.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "User Profile Success",
            data={
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "phone": "555-123-4567",
                "address": "123 Main St, Anytown, US",
                "oidc_provider": "google",
                "created_at": "2025-01-15T08:30:00Z",
                "updated_at": "2025-06-01T14:45:00Z",
            },
            message="User profile retrieved successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[401]),
    },
}


# Schema for updating user profile
update_user_profile_schema = {
    "summary": "Update User Profile",
    "description": "Update the profile information for the authenticated user.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "User Profile Updated Success",
            data={
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "phone": "555-987-6543",  # Updated
                "address": "456 Oak Ave, Sometown, US",  # Updated
                "oidc_provider": "google",
                "created_at": "2025-01-15T08:30:00Z",
                "updated_at": "2025-06-04T10:15:00Z",  # Updated
            },
            message="User profile updated successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[400, 401]),
    },
    "examples": [
        OpenApiExample(
            "Update Contact Info",
            summary="Update contact information",
            description="Update phone number and address.",
            value={
                "first_name": "John",
                "last_name": "Doe",
                "phone": "555-987-6543",
                "address": "456 Oak Ave, Sometown, US",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Update Name Only",
            summary="Update user's name",
            description="Update first and last name only.",
            value={"first_name": "Johnny", "last_name": "Doe"},
            request_only=True,
        ),
    ],
}


# Schema for getting OpenID Connect token
oidc_token_schema = {
    "summary": "Exchange for JWT Token",
    "description": "Exchange an OpenID Connect token for a JWT token for API access.",
    "responses": {
        status.HTTP_200_OK: {
            "schema": {
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "string",
                        "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    },
                    "access": {
                        "type": "string",
                        "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    },
                },
            },
        },
        **get_standard_responses(include=[401]),
    },
}
