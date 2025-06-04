from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiTypes
from rest_framework import status


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


list_products_schema = {
    "summary": "List Products",
    "description": """
    Retrieve a list of all products available in the store.
    Optional filtering by category is available through query parameters.
    """,
    "parameters": [
        OpenApiParameter(
            name="category_id",
            description="Filter products by category ID",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
    ],
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "Product List Success",
            data=[
                {
                    "id": 1,
                    "name": "Organic Bananas",
                    "slug": "organic-bananas",
                    "category": {
                        "id": 3,
                        "name": "Fruits",
                        "slug": "fruits",
                        "parent": 2,
                    },
                    "description": "Fresh organic bananas, locally sourced",
                    "price": "2.99",
                    "stock": 50,
                },
                {
                    "id": 2,
                    "name": "Whole Wheat Bread",
                    "slug": "whole-wheat-bread",
                    "category": {
                        "id": 5,
                        "name": "Bread",
                        "slug": "bread",
                        "parent": 4,
                    },
                    "description": "Freshly baked whole wheat bread",
                    "price": "3.49",
                    "stock": 20,
                },
            ],
            message="Products retrieved successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[401, 404]),
    },
}


retrieve_product_schema = {
    "summary": "Get Product Details",
    "description": "Retrieve detailed information about a specific product by ID.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "Product Details Success",
            data={
                "id": 1,
                "name": "Organic Bananas",
                "slug": "organic-bananas",
                "category": {
                    "id": 3,
                    "name": "Fruits",
                    "slug": "fruits",
                    "parent": 2,
                },
                "description": "Fresh organic bananas, locally sourced",
                "price": "2.99",
                "stock": 50,
            },
            message="Product retrieved successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[404]),
    },
}


category_average_price_schema = {
    "summary": "Calculate Average Price for Category",
    "description": """
    Calculate the average price of all products in a specified category.
    Optionally include products from all subcategories in the calculation.
    """,
    "parameters": [
        OpenApiParameter(
            name="category_id",
            description="Category ID to calculate average price for",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="include_subcategories",
            description="Whether to include products from subcategories (default: false)",
            required=False,
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
        ),
    ],
    "responses": {
        status.HTTP_200_OK: {
            "schema": {
                "type": "object",
                "properties": {
                    "average_price": {"type": "number", "format": "float", "example": 3.99},
                },
            },
            "examples": [
                {
                    "name": "Produce Category Average",
                    "value": {"average_price": 3.99},
                }
            ],
        },
        **get_standard_responses(include=[400, 404]),
    },
    "examples": [
        OpenApiExample(
            "Fruits Category Only",
            summary="Calculate average price for Fruits category only",
            description="Get average price for products directly in the Fruits category.",
            value={
                "category_id": 3,
                "include_subcategories": False,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Produce with Subcategories",
            summary="Calculate for Produce including subcategories",
            description=(
                "Get average price for all products in Produce and its subcategories "
                "(Fruits, Vegetables, etc.)"
            ),
            value={
                "category_id": 2,
                "include_subcategories": True,
            },
            request_only=True,
        ),
    ],
}


list_categories_schema = {
    "summary": "List Categories",
    "description": "Retrieve a list of all product categories with their hierarchical structure.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "Category List Success",
            data=[
                {
                    "id": 1,
                    "name": "All Products",
                    "slug": "all-products",
                    "parent": None,
                },
                {
                    "id": 2,
                    "name": "Produce",
                    "slug": "produce",
                    "parent": 1,
                },
                {
                    "id": 3,
                    "name": "Fruits",
                    "slug": "fruits",
                    "parent": 2,
                },
                {
                    "id": 4,
                    "name": "Bakery",
                    "slug": "bakery",
                    "parent": 1,
                },
                {
                    "id": 5,
                    "name": "Bread",
                    "slug": "bread",
                    "parent": 4,
                },
            ],
            message="Categories retrieved successfully",
            status_code=200,
        ),
    },
}


retrieve_category_schema = {
    "summary": "Get Category Details",
    "description": "Retrieve detailed information about a specific category by ID.",
    "responses": {
        status.HTTP_200_OK: create_success_example(
            "Category Details Success",
            data={
                "id": 3,
                "name": "Fruits",
                "slug": "fruits",
                "parent": 2,
            },
            message="Category retrieved successfully",
            status_code=200,
        ),
        **get_standard_responses(include=[404]),
    },
}
