from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)
        return user

    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    TYPE = (
        ('customer', 'Customer'),
        ('seller', 'Seller') 
    )

    username=None
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='user_dp/', blank=True, null=True)
    contact_number = PhoneNumberField(blank=True, null=True, unique=True)
    user_role = models.CharField(choices = TYPE, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = UserManager()
