from django.core.management.base import BaseCommand
from product.models import Product

class Command(BaseCommand):
    help = 'Deletes all product entries from the database'

    def handle(self, *args, **options):
        # Count the entries to report how many were deleted
        count = Product.objects.count()
        # Delete all entries
        Product.objects.all().delete()
        # Success message
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} products'))
