from rest_framework import viewsets
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer

# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

class CustomerList(generics.ListAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()