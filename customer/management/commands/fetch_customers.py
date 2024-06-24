from django.core.management.base import BaseCommand
from customer.models import Customer
from customer.scripts.get_customers import fetch_all_customers

class Command(BaseCommand):
    help = 'Fetch and store Lightspeed customers'

    def handle(self, *args, **kwargs):
        customers = fetch_all_customers()
        count_new = 0
        count_updated = 0
        for customer_data in customers:
            customer, created = Customer.objects.update_or_create(
                customer_id=customer_data['customer_id'],
                defaults=customer_data
            )
            if created:
                count_new += 1
                self.stdout.write(self.style.SUCCESS(f'Created new customer: {customer.first_name} {customer.last_name}'))
            else:
                count_updated += 1
                self.stdout.write(f'Updated existing customer: {customer.first_name} {customer.last_name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored customers. New: {count_new}, Updated: {count_updated}'))
