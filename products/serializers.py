from products.models import (
    Product, 
    Colors, 
    SubCategory, 
    ProductCategory
)
from rest_framework import serializers

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ['is_deleted']


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        exclude = ['is_deleted']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ['is_deleted']


# class CustomField(serializers.Field):
#     def get_attribute(self, instance):
#         return instance

#     def to_representation(self, instance):
#         # calculate the value of the field based on other fields
#         value = str(instance.created_at) + '-' + str(instance.id)

#         return value

class ProductSerializer(serializers.ModelSerializer):
    prod = ProductCategorySerializer(many = True, read_only = True)
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['is_deleted']
    



