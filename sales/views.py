from rest_framework import viewsets
from rest_framework import generics
from .models import Orders, OrderProduct
from .serializers import OrderSerializer, OrderProductSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrderProductViewSet(viewsets.ModelViewSet):
#     queryset = OrderProduct.objects.all()
#     serializer_class = OrderProductSerializer
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class OrderProductList(generics.ListAPIView):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()