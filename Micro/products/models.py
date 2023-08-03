from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Micro.custom_configs import handle_product_attachment_upload, get_nano_id , protected_storage




# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # stripe_product_id
    # stripe_price_id
    image = models.ImageField(upload_to='products',blank=True)
    name = models.CharField(max_length=12)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price = models.IntegerField()
    price_change_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price != self.og_price:
            self.og_price = self.price
            self.stripe_price = int(self.price * 100)
            self.price_change_timestamp = timezone.now()
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name




class ProductAttachment(models.Model):
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    handle = models.SlugField(unique=True)
    file = models.FileField(upload_to=handle_product_attachment_upload,storage=protected_storage)
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return self.handle