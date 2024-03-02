from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Order, OrderItem, Discount, Tax


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class DiscountSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Discount
        fields = "__all__"


class TaxSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Tax
        fields = "__all__"
