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


# Schema for listing user's orders
list_orders_schema = {
    "summary": "List User Orders",
    "description": "Retrieve a list of all orders placed by the authenticated user.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "User Orders Success",
            data=[
                {
                    "id": 1,
                    "order_number": "ORD-AB12CD",
                    "total_amount": "42.99",
                    "shipping_address": "123 Nairobi, Kenya",
                    "created_at": "2025-06-01T10:30:00Z",
                },
                {
                    "id": 2,
                    "order_number": "ORD-EF34GH",
                    "total_amount": "29.45",
                    "shipping_address": "456 kasarani, Kenya",
                    "created_at": "2025-06-03T14:15:00Z",
                },
            ],
            message="Orders retrieved successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[401]),
    },
}


# Schema for retrieving a single order
retrieve_order_schema = {
    "summary": "Get Order Details",
    "description": "Retrieve detailed information about a specific order by ID.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "Order Details Success",
            data={
                "id": 1,
                "order_number": "ORD-AB12CD",
                "total_amount": "42.99",
                "shipping_address": "123 Westlands, Nairobi, Kenya",
                "created_at": "2025-06-01T10:30:00Z",
            },
            message="Order retrieved successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[401, 404]),
    },
}


# Schema for creating a new order
create_order_schema = {
    "summary": "Create New Order",
    "description": """
    Create a new order with the specified items.
    Stock levels are automatically checked and updated.
    """,
    "responses": {
        status.HTTP_201_CREATED: create_success_example(
            "Order Created Success",
            data={
                "id": 3,
                "order_number": "ORD-IJ56KL",
                "total_amount": "55.97",
                "shipping_address": "789 Moi Avenue, Nairobi, Kenya",
                "created_at": "2025-06-04T09:45:00Z",
            },
            message="Order created successfully",
            status_code=201,
        ),
        **get_standard_responses(include=[400, 401]),
    },
    "examples": [
        OpenApiExample(
            "Simple Order",
            summary="Create order with single item",
            description="Basic order with one product.",
            value={
                "shipping_address": "123 Kenyatta Avenue, Nairobi, Kenya",
                "items": [{"product_id": 1, "quantity": 2}],
            },
            request_only=True,
        ),
        OpenApiExample(
            "Multiple Items Order",
            summary="Create order with multiple items",
            description="Order with multiple products of different quantities.",
            value={
                "shipping_address": "456 Ngong Road, Kilimani, Nairobi, Kenya",
                "items": [
                    {"product_id": 1, "quantity": 1},
                    {"product_id": 2, "quantity": 3},
                    {"product_id": 5, "quantity": 2},
                ],
            },
            request_only=True,
        ),
    ],
}
