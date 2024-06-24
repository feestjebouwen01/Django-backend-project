import requests
from dateutil import parser
from django.core.management.base import BaseCommand
from django.db import transaction
from sales.models import Orders
from customer.models import Customer
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = 'a25fc6aecf551494d9cd4f81c40fea29'
API_SECRET = '9e056b7102ebb125e8482e5dcf296ed3'
CLUSTER_URL = 'api.webshopapp.com'
SHOP_LANGUAGE = 'nl'

def get_customers(customer_id):
    """Fetch a specific customer from the API."""
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/customers/{customer_id}.json'
    response = requests.get(url)
    if response.status_code == 200:
        customer = response.json()['customer']
        return {
            'customer_id': customer['id'],
            'first_name': customer.get('firstname', ''),
            'last_name': customer.get('lastname', ''),
            'email': customer.get('email', ''),
            'created_at': parser.parse(customer['createdAt']) if customer.get('createdAt') else None,
            'updated_at': parser.parse(customer['updatedAt']) if customer.get('updatedAt') else None
        }, True
    else:
        logging.error(f"Failed to fetch customer {customer_id}: {response.status_code}, {response.text}")
        return None, False

def get_orders(page=1):
    """ Fetch a page of orders from the API. """
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/orders.json?page={page}&limit=250'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        orders = data['orders']
        has_more = page < 100  # Only fetch up to 100 pages
        return orders, has_more
    else:
        logging.error(f"Failed to fetch orders: {response.status_code}, {response.text}")
        return [], False

def fetch_all_orders():
    page = 1
    while page <= 100:
        orders, has_more = get_orders(page)
        if not orders:
            break
        for order in orders:
            customer_id = order['customer']['resource']['id']
            customer, created = Customer.objects.get_or_create(customer_id=customer_id)
            if not customer:
                customer_data, success = get_customers(customer_id)
                if success:
                    customer = Customer.objects.create(**customer_data)

            order_instance, created = Orders.objects.update_or_create(
                order_id=order['id'],
                defaults={
                    'number': order['number'],
                    'status': order['status'],
                    'channel': order['channel'],
                    'created_at': parser.parse(order['createdAt']),
                    'price_incl': order['priceIncl'],
                    'price_excl': order['priceExcl'],
                    'payment_status': order['paymentStatus'],
                    'firstname': order['firstname'],
                    'lastname': order['lastname'],
                    'customer': customer
                }
            )
            if created:
                logging.info(f'Created order {order["number"]}')
            else:
                logging.info(f'Updated order {order["number"]}')
        if not has_more:
            break
        page += 1

class Command(BaseCommand):
    help = 'Fetch and store Lightspeed orders'

    @transaction.atomic
    def handle(self, *args, **options):
        fetch_all_orders()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored orders'))
