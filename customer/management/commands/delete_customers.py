from django.core.management.base import BaseCommand
from customer.models import Customer

class Command(BaseCommand):
    help = 'Deletes all customer entries from the database'

    def handle(self, *args, **options):
        # Count the entries to report how many were deleted
        count = Customer.objects.count()
        # Delete all entries
        Customer.objects.all().delete()
        # Success message
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} customers'))
