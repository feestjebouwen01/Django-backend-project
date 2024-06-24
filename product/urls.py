from django.urls import path
from .views import ProductList

app_name = 'product_api'



urlpatterns = [
   path('', ProductList.as_view(), name='productlistcreate'),
]