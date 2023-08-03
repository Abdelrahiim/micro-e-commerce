from django.contrib import admin
from Micro.products.models import Product, ProductAttachment
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductAttachment)