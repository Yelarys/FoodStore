from rest_framework import serializers
from .models import Order, Restaurant
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class OrderModelSerializer(serializers.ModelSerializer):
    customer_info = UserModelSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['customer_info', 'delivery_date', 'product', 'payment_method', 'order_status', 'quantity']


class RestaurantModelSerializer(serializers.ModelSerializer):
    owner = UserModelSerializer(read_only=True)
    class Meta:
        model = Restaurant
        fields = ['type', 'name', 'city', 'address', 'info', 'owner']