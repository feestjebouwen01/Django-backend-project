import requests
from dateutil import parser
from django.db import transaction
from sales.models import Orders, Customer

API_KEY = 'a25fc6aecf551494d9cd4f81c40fea29'
API_SECRET = '9e056b7102ebb125e8482e5dcf296ed3'
CLUSTER_URL = 'api.webshopapp.com'
SHOP_LANGUAGE = 'nl'

def get_customer_by_api_id(api_id):
    customer_url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/customers/{api_id}.json'
    response = requests.get(customer_url)
    if response.status_code == 200:
        customer_data = response.json()['customer']
        customer, created = Customer.objects.get_or_create(
            customer_id=customer_data['id'],
            defaults={
                'first_name': customer_data.get('firstname', ''),
                'last_name': customer_data.get('lastname', ''),
                'email': customer_data.get('email', ''),
                'created_at': parser.parse(customer_data['createdAt']) if customer_data.get('createdAt') else None,
                'updated_at': parser.parse(customer_data['updatedAt']) if customer_data.get('updatedAt') else None
            }
        )
        return customer
    else:
        print(f"Failed to fetch customer {api_id}: {response.status_code}")
        return None

def get_orders(page=1):
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/orders.json?page={page}&limit=250'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['orders']
    else:
        print("Failed to fetch orders:", response.status_code, response.text)
        return []

def fetch_all_orders():
    page = 1
    while True:
        orders = get_orders(page)
        if not orders:
            break
        for order in orders:
            try:
                customer = get_customer_by_api_id(order['customer']['resource']['id'])
                if customer:
                    order_instance, created = Orders.objects.update_or_create(
                        order_id=order['id'],
                        defaults={
                            'number': order['number'],
                            'status': order['status'],
                            'channel': order['channel'],
                            'created_at': parser.parse(order['createdAt']),
                            'price_incl': float(order['priceIncl']),
                            'price_excl': float(order['priceExcl']),
                            'payment_status': order.get('paymentStatus', ''),
                            'firstname': order.get('firstname', ''),
                            'lastname': order.get('lastname', ''),
                            'addressShippingStreet': order.get('addressShippingStreet', ''),
                            'addressShippingNumber': order.get('addressShippingNumber', ''),
                            'addressShippingExtension': order.get('addressShippingExtension', ''),
                            'addressShippingZipcode': order.get('addressShippingZipcode', ''),
                            'addressShippingCity': order.get('addressShippingCity', ''),
                            'shipping_country_code': order.get('addressShippingCountry', {}).get('code', ''),
                            'customer': customer,
                            'latitude': None,  # Placeholder for later geocoding
                            'longitude': None,  # Placeholder for later geocoding
                            'customer_URL': order['customer']['resource']['link'],
                            'products_URL': order['products']['resource']['link'],
                        }
                    )
                    if created:
                        print(f"Created new order: {order_instance.number}")
                    else:
                        print(f"Updated existing order: {order_instance.number}")
            except Exception as e:
                print(f"Failed to process order {order['id']}: {str(e)}")
        page += 1
