from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    shipping_country_code = models.CharField(max_length=10)
    shipping_zipcode = models.CharField(max_length=20)
    shipping_city = models.CharField(max_length=100)
    shipping_number = models.CharField(max_length=100)
    shipping_street = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price_incl = models.DecimalField(max_digits=10, decimal_places=2)  # New field

    def __str__(self):
        return self.order_id
