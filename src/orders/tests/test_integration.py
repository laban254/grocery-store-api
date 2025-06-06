import json
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Order


@pytest.mark.django_db
class TestOrderingProcess:
    """Integration tests for the entire ordering process."""

    @patch("orders.serializers.send_order_confirmation_sms")
    def test_complete_order_process(self, mock_sms_task, authenticated_client, products, user):
        """Test the complete order process from creation to confirmation."""
        initial_stocks = {p.id: p.stock for p in products}

        order_data = {
            "shipping_address": "123 Integration Test St, Nairobi, Kenya",
            "items": [
                {"product_id": products[0].id, "quantity": 2},
                {"product_id": products[1].id, "quantity": 3},
            ],
        }

        url = reverse("order-list")
        response = authenticated_client.post(
            url, data=json.dumps(order_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        order_id = response.data["id"]

        order = Order.objects.get(id=order_id)
        assert order.user == user
        assert order.shipping_address == "123 Integration Test St, Nairobi, Kenya"
        assert order.status == "pending"

        assert order.items.count() == 2

        for item in order.items.all():
            if item.product.id == products[0].id:
                assert item.quantity == 2
                assert item.price == products[0].price
            elif item.product.id == products[1].id:
                assert item.quantity == 3
                assert item.price == products[1].price

        expected_total = (products[0].price * 2) + (products[1].price * 3)
        assert order.total_amount == expected_total

        for product in products:
            product.refresh_from_db()

        assert products[0].stock == initial_stocks[products[0].id] - 2
        assert products[1].stock == initial_stocks[products[1].id] - 3

        mock_sms_task.delay.assert_called_once_with(order.id)

        detail_url = reverse("order-detail", args=[order.id])
        detail_response = authenticated_client.get(detail_url)

        assert detail_response.status_code == status.HTTP_200_OK
        assert detail_response.data["order_number"] == order.order_number

        list_response = authenticated_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK

        order_ids = [order["id"] for order in list_response.data]
        assert order.id in order_ids

    @patch("orders.signals.send_order_status_update_sms")
    def test_order_status_update_flow(self, mock_status_task, db, order):
        """Test the order status update flow from pending to delivered."""
        assert order.status == "pending"

        order.status = "processing"
        order.save()

        mock_status_task.delay.assert_called_once_with(order.id, "processing")
        mock_status_task.delay.reset_mock()

        order.status = "shipped"
        order.save()

        mock_status_task.delay.assert_called_once_with(order.id, "shipped")
        mock_status_task.delay.reset_mock()

        order.status = "delivered"
        order.save()

        mock_status_task.delay.assert_called_once_with(order.id, "delivered")

    @patch("orders.serializers.send_order_confirmation_sms")
    def test_insufficient_stock_handling(self, mock_sms_task, authenticated_client, products):
        """Test that the system properly handles orders with insufficient stock."""
        products[0].stock = 1
        products[0].save()

        order_data = {
            "shipping_address": "123 Integration Test St, Nairobi, Kenya",
            "items": [{"product_id": products[0].id, "quantity": 10}],
        }

        url = reverse("order-list")
        response = authenticated_client.post(
            url, data=json.dumps(order_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Not enough stock" in str(response.data)

        assert Order.objects.count() == 0

        products[0].refresh_from_db()
        assert products[0].stock == 1

        mock_sms_task.delay.assert_not_called()
