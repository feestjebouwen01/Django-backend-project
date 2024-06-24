# from django.core.management.base import BaseCommand
# from sales.models import Orders
# from sales.scripts.fetching_orders1 import fetch_all_orders

# class Command(BaseCommand):
#     help = 'Fetch and store Shopify orders'

#     def handle(self, *args, **kwargs):
#         orders = fetch_all_orders()
#         for order_data in orders:
#             Orders.objects.update_or_create(order_id=order_data['order_id'], defaults=order_data)
#         self.stdout.write(self.style.SUCCESS('Successfully fetched and stored orders'))
from django.core.management.base import BaseCommand
from django.db import transaction
from sales.models import Orders
from sales.scripts.fetching_orders4 import fetch_all_orders

class Command(BaseCommand):
    help = 'Fetch and store Shopify orders'

    def handle(self, *args, **kwargs):
        try:
            orders = fetch_all_orders()  # This should return a list of dictionaries
            for order_data in orders:
                order, created = Orders.objects.update_or_create(
                    order_id=order_data['order_id'],
                    defaults=order_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new order: {order.number}'))
                else:
                    self.stdout.write(f'Updated existing order: {order.number}')
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored orders'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))


