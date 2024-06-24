from django.urls import path
from .views import CustomerList

app_name = 'customer_api'



urlpatterns = [
   path('', CustomerList.as_view(), name='listcreate'),
]