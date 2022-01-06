from .models import Order, OrderItems, Customer, FoodItem
from rest_framework import serializers
from user_control.serializers import CustomUserSerializer


class FoodItemSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    # created_by_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = FoodItem
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    food_item_id = serializers.CharField(write_only=True, required=True)
    order = serializers.CharField(read_only=True)
    order_id = serializers.CharField(write_only=True)

    class Meta:
        model = OrderItems
        fields = "__all__"


class OrderItemsDataSerializer(serializers.Serializer):
    food_item_id = serializers.CharField()
    quantity = serializers.CharField()


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    order_order_items = OrderItemsSerializer(read_only=True, many=True)
    order_items_data = OrderItemsDataSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = "__all__"

