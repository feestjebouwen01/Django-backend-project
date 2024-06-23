from django.db import models
from product.models import Product
from customer.models import Customer

class OrderProduct(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_products')
    brand_title = models.CharField(max_length=255)
    product_title = models.CharField(max_length=255)
    variant_title = models.CharField(max_length=255)
    quantity_ordered = models.IntegerField()
    article_code = models.CharField(max_length=100)
    ean = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    price_excl = models.DecimalField(max_digits=10, decimal_places=2)
    price_incl = models.DecimalField(max_digits=10, decimal_places=2)
    product_url = models.URLField()

    def __str__(self):
        return f"{self.product_title} ({self.quantity_ordered} units)"

class Orders(models.Model):

    class WebshopObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(channel='main')
    
    class ApiObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(channel='api')

    STATUS_CHOICES = [
        ('on_hold', 'On_hold'),
        ('processing_awaiting_payment', 'Processing_awaiting_payment'),
        ('processing_awaiting_shipment', 'Processing_awaiting_shipment'),
        ('processing_awaiting_pickup', 'Processing_awaiting_pickup'),
        ('processing_ready_for_pickup','Processing_ready_for_pickup'),
        ('completed','Completed'),
        ('completed_shipped','Completed_shipped'),
        ('completed_picked_up','Completed_picked_up'),
        ('cancelled','Cancelled'),
    ]
    CHANNEL_CHOICES = [
        ('api', 'API'),
        ('main', 'Main'),
    ]
    PAYMENT_CHOICES = [
        ('not_paid', 'Not_paid'),
        ('partially_paid', 'Partially_paid'),
        ('paid', 'Paid'),
        ('cancelled','Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    created_at = models.DateTimeField()
    price_incl = models.DecimalField(max_digits=10, decimal_places=2)
    price_excl = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    firstname = models.CharField(max_length=50, blank= True, null=True)
    lastname = models.CharField(max_length=50, blank= True, null=True)

    #Address for geocoding & possibly showing on frontend
    addressShippingStreet = models.CharField(max_length=100, blank=True, null=True)
    addressShippingNumber = models.CharField(max_length=20, blank=True, null=True)
    addressShippingExtension = models.CharField(max_length=10, blank=True, null=True)
    addressShippingZipcode = models.CharField(max_length=20, blank=True, null=True)
    addressShippingCity = models.CharField(max_length=100, blank=True, null=True)
    shipping_country_code = models.CharField(max_length=3)

    #Geocoding location to latitude & longtitude so I can plot it on a map
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    #URL for other tables, used to call the other api's for fetching data
    customer_URL = models.CharField(max_length=250)
    products_URL = models.CharField(max_length=250)

    #link to other tables
    products = models.ManyToManyField('product.Product', through=OrderProduct)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='orders')

    #custom Object Manager
    webshopObjects = WebshopObjects()
    apiObjects = ApiObjects()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.number} - {self.status}"