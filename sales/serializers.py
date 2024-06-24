from rest_framework import serializers
from .models import Orders, OrderProduct
from customer.serializers import CustomerSerializer
from product.serializers import ProductSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity_ordered', 'price_excl', 'price_incl']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    order_products = OrderProductSerializer(source='order_products_set', many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['order_id', 'number', 'status', 'customer', 'order_products', 'created_at', 'channel', 'price_incl', 'price_excl']
