from rest_framework import viewsets
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()