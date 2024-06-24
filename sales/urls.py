from django.urls import path
from .views import OrderList, OrderProductList

app_name = 'sales_api'



urlpatterns = [
   path('', OrderList.as_view(), name='Orderlistcreate'),
   path('product/', OrderProductList.as_view(), name='OrderProductlistcreate'),
]