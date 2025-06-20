import uuid

from rest_framework import serializers

from products.models import Product

from .models import Order, OrderItem
from .tasks import send_order_confirmation_sms


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating order items.
    """

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )

    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing orders.
    """

    class Meta:
        model = Order
        fields = ["id", "order_number", "total_amount", "shipping_address", "created_at"]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for making an order.
    """

    shipping_address = serializers.CharField()
    items = OrderItemCreateSerializer(many=True)

    def validate(self, attrs):
        request = self.context.get("request")
        if not request.user.phone:
            raise serializers.ValidationError(
                "Please update your profile with a phone number before placing an order. "
                "We need your phone number to send order updates via SMS."
            )
        return attrs

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("An order must contain at least one item.")

        for item in value:
            product = item["product"]
            quantity = item["quantity"]

            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Available: {product.stock}"
                )

        return value

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user

        order_number = f"ORD-{uuid.uuid4().hex[:6].upper()}"

        total_amount = sum(
            item_data["product"].price * item_data["quantity"] for item_data in items_data
        )

        order = Order.objects.create(
            user=user,
            order_number=order_number,
            total_amount=total_amount,
            shipping_address=validated_data["shipping_address"],
        )

        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=product.price
            )
            product.stock -= quantity
            product.save()

        send_order_confirmation_sms.delay(order.id)

        return order
