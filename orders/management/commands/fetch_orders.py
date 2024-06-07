from django.core.management.base import BaseCommand
from orders.models import Order
from orders.scripts.fetch_orders import fetch_all_orders

class Command(BaseCommand):
    help = 'Fetch and store Shopify orders'

    def handle(self, *args, **kwargs):
        orders = fetch_all_orders()
        for order_data in orders:
            Order.objects.update_or_create(order_id=order_data['order_id'], defaults=order_data)
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored orders'))
