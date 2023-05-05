from products.models import Product, Colors, SubCategory, ProductCategory
from rest_framework import serializers

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = "__all__"

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


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
    
class TopCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs




