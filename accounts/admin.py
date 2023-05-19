from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_filter = ["user_role", "last_login", "is_superuser", "date_joined", "is_active",]

admin.site.register(User, PersonAdmin)
# admin.site.register(User)