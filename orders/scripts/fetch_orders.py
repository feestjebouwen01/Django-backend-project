import json
import requests
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from orders.models import Order

API_KEY = 'a25fc6aecf551494d9cd4f81c40fea29'
API_SECRET = '9e056b7102ebb125e8482e5dcf296ed3'
CLUSTER_URL = 'api.webshopapp.com'
SHOP_LANGUAGE = 'nl'
GEOCODER_API_KEY = '2aae229e1b87435b808711231e955d95'

geocoder = OpenCage(GEOCODER_API_KEY, timeout=10)

def get_orders(page=1):
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/orders.json?page={page}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['orders']
    else:
        print("Failed to fetch orders:", response.status_code, response.text)
        return []

def fetch_all_orders():
    page = 1
    all_orders = []
    max_pages = 2

    while page <= max_pages:
        orders = get_orders(page)
        if not orders:
            break
        for order in orders:
            address = f"{order['addressShippingNumber']} {order['addressShippingStreet']}, {order['addressShippingCity']}, {order['addressShippingCountry']['code']}"
            location = None
            attempts = 0
            while attempts < 3:
                try:
                    location = geocoder.geocode(address)
                    if location:
                        break
                except (GeocoderTimedOut, GeocoderServiceError) as e:
                    attempts += 1
                    print(f"Geocoding attempt {attempts} failed for address: {address} with error: {e}")
                    time.sleep(2)

            order_data = {
                'order_id': order['id'],
                'created_at': order['createdAt'],
                'shipping_country_code': order['addressShippingCountry']['code'],
                'shipping_zipcode': order['addressShippingZipcode'],
                'shipping_city': order['addressShippingCity'],
                'shipping_number': order['addressShippingNumber'],
                'shipping_street': order['addressShippingStreet'],
                'latitude': location.latitude if location else None,
                'longitude': location.longitude if location else None,
                'price_incl': order.get('priceIncl', 0.0)
            }
            all_orders.append(order_data)
        page += 1

    return all_orders

class Command(BaseCommand):
    help = 'Fetch and store Shopify orders'

    def handle(self, *args, **options):
        orders = fetch_all_orders()
        for order_data in orders:
            Order.objects.update_or_create(order_id=order_data['order_id'], defaults=order_data)
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored orders'))
