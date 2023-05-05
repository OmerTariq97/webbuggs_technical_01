from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL
# Create your models here.

class MyModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_deleted=True)

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    image = models.ImageField(blank = True, null = True)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
                                    related_name="created_sub_categories")
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE,
                                    related_name="updated_sub_categories")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    objects = MyModelManager()


class Colors(models.Model):
    name = models.CharField(max_length = 50)
    color_code = models.CharField(max_length = 25)
    created_at = models.DateTimeField(default = timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    objects = MyModelManager()


class Product(models.Model):
    title = models.CharField(max_length = 100)
    category = models.ForeignKey("SubCategory", on_delete = models.CASCADE)
    description = models.CharField(max_length = 200)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User,on_delete = models.CASCADE, 
                                    related_name="created_products")
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, 
                                    related_name="updated_products")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)
    sku = models.CharField(max_length=20,blank = True ,editable=False)
    colors = models.ManyToManyField("Colors")        
    is_deleted = models.BooleanField(default=False)

    objects = MyModelManager()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.sku:
            self.sku = self.created_at.strftime('%Y%m%d') + '-' + str(self.id)
            self.save()

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    image = models.ImageField(blank = True, null = True)
    description = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod', null= True, blank= True)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
                                    related_name="created_product_category")
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, 
                                    related_name="updated_product_category")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)
    is_deleted = models.BooleanField(default=False)

    objects = MyModelManager()
