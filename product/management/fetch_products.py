from django.core.management.base import BaseCommand
from product.models import Product
from product.scripts.get_products import fetch_all_products

class Command(BaseCommand):
    help = 'Fetch and store Lightspeed products'

    def handle(self, *args, **kwargs):
        products = fetch_all_products()
        for product_data in products:
            product, created = Product.objects.update_or_create(
                product_id=product_data['product_id'],
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new product: {product.title}'))
            else:
                self.stdout.write(f'Updated existing product: {product.title}')

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored products'))
