from django.db import models

class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_visible = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    image_url = models.URLField(max_length=1024)

    def __str__(self):
        return self.title
