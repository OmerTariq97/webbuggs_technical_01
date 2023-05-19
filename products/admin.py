from django.contrib import admin
from .models import Product, Colors, ProductCategory, SubCategory
# Register your models here.
admin.site.register(Product)
admin.site.register(Colors)
admin.site.register(ProductCategory)
admin.site.register(SubCategory)