import json
import requests
import time
from dateutil import parser
from django.conf import settings
from django.core.management.base import BaseCommand
from product.models import Product

API_KEY = 'a25fc6aecf551494d9cd4f81c40fea29'
API_SECRET = '9e056b7102ebb125e8482e5dcf296ed3'
CLUSTER_URL = 'api.webshopapp.com'
SHOP_LANGUAGE = 'nl'


def get_products(page=1):
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/products.json?page={page}&limit=250'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['products']
    else:
        print("Failed to fetch products:", response.status_code, response.text)
        return []

def fetch_all_products():
    page = 1
    all_products = []
    max_pages = 1

    while page <= max_pages:
        products = get_products(page)
        if not products:
            break
        for product in products:

            product_data = {
                'product_id': product['id'],
                'created_at': parser.parse(product['createdAt']),
                'updated_at': parser.parse(product['updatedAt']),
                'is_visible': product['isVisible'],
                'title': product['title'],
                'description': product['description'],
                'content': product['content'],
                'image_url': product['image']['src'] if 'image' in product else None
            }
            all_products.append(product_data)
        page += 1

    return all_products

class Command(BaseCommand):
    help = 'Fetch and store Lightspeed orders'

    def handle(self, *args, **options):
        products = fetch_all_products()
        for product_data in products:
            Product.objects.update_or_create(product_id=product_data['product_id'], defaults=product_data)
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored products'))
