from django.core.management.base import BaseCommand
from sales.models import Orders

class Command(BaseCommand):
    help = 'Deletes all orders entries from the database'

    def handle(self, *args, **options):
        # Count the entries to report how many were deleted
        count = Orders.objects.count()
        # Delete all entries
        Orders.objects.all().delete()
        # Success message
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} orders'))
