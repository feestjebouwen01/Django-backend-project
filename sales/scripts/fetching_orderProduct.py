import requests
from dateutil import parser
from django.db import transaction
from sales.models import Orders, OrderProduct, Customer
from product.models import Product

API_KEY = 'a25fc6aecf551494d9cd4f81c40fea29'
API_SECRET = '9e056b7102ebb125e8482e5dcf296ed3'
CLUSTER_URL = 'api.webshopapp.com'
SHOP_LANGUAGE = 'nl'

def get_product_details(order_id):
    """ Fetch products for a given order from the API. """
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/orders/{order_id}/products.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('products', [])
    else:
        print(f"Failed to fetch products for order {order_id}: {response.status_code}")
        return []

def fetch_all_orders():
    page = 1
    while True:
        orders = get_orders(page)
        if not orders:
            break
        for order in orders:
            customer = get_customer_by_api_id(order['customer']['resource']['id'])
            if not customer:
                continue  # Skip order if no customer found
            with transaction.atomic():
                order_instance, created = Orders.objects.update_or_create(
                    order_id=order['id'],
                    defaults={...}  # Fill in the fields as you currently do
                )
                products = get_product_details(order['id'])
                for product in products:
                    Product.objects.update_or_create(
                        sku=product['sku'],
                        defaults={
                            'brand_title': product.get('brand'),
                            'product_title': product.get('title'),
                            'variant_title': product.get('variant_title'),
                            'quantity_ordered': product.get('quantity'),
                            'article_code': product.get('article_code'),
                            'ean': product.get('ean'),
                            'price_excl': product.get('price_excl'),
                            'price_incl': product.get('price_incl'),
                            'product_url': product.get('url')
                        }
                    )
                if created:
                    print(f"Created new order: {order_instance.number}")
                else:
                    print(f"Updated existing order: {order_instance.number}")
        page += 1

# Call to fetch all orders and products
fetch_all_orders()
