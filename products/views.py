from .models import ( 
    Product, 
    Colors, 
    SubCategory, 
    ProductCategory
)
from .serializers import (
    ProductSerializer, 
    ColorsSerializer, 
    SubCategorySerializer, 
    ProductCategorySerializer
)
from django.core.exceptions import ValidationError
from accounts.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework.authentication import (
    BasicAuthentication, 
    SessionAuthentication, 
    TokenAuthentication
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from django.db.models import Q
from django.db.models import Count
# Create your views here.

# class CaseInsensitiveSubstringFilterBackend(BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         filter_title = request.query_params.get('title')
#         filter_descripton = request.query_params.get('description')
#         filter_sku = request.query_params.get('sku')

        # if search_terms:
        #     q = Q()
        #     for term in search_terms:
        #         q |= Q(title__icontains=term) # Replace "name" with the field you want to search
        #     queryset = queryset.filter(q)
        # return queryset
        # if filter_title:
        #     queryset = queryset.filter(title__icontains=filter_title)
        # elif filter_descripton:
        #     queryset = queryset.filter(description__icontains=filter_descripton)
        # elif filter_sku:
        #     queryset = queryset.filter(sku__icontains=filter_sku)

        # return queryset


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['title','sku','description']
    search_fields = ['title','sku','description']

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'msg':'deleted'})

    # def list(self, request):
    #     my_filter_SKU = self.request.query_params.get('filter_SKU')
    #     my_filter_title = self.request.query_params.get('filter_title')
    #     my_filter_description = self.request.query_params.get('filter_description')

    #     queryset = self.get_queryset()
    #     if my_filter_SKU:
    #         queryset = queryset.filter(sku__icontains=my_filter_SKU)
    #     elif my_filter_title:
    #         queryset = queryset.filter(title__icontains=my_filter_title)
    #     elif my_filter_description:
    #         queryset = queryset.filter(description__icontains=my_filter_description)

    #     serializer = self.get_serializer(queryset, many = True)
    #     return Response(serializer.data)

    # @action(detail=False, methods=['get'])
    # def filter(self, request):
    #     my_filter_SKU = self.request.query_params.get('filter_SKU')
    #     my_filter_title = self.request.query_params.get('filter_title')
    #     my_filter_description = self.request.query_params.get('filter_description')

    #     queryset = self.get_queryset()
    #     if my_filter_SKU:
    #         queryset = queryset.filter(sku__icontains=my_filter_SKU)
    #     elif my_filter_title:
    #         queryset = queryset.filter(title__icontains=my_filter_title)
    #     elif my_filter_description:
    #         queryset = queryset.filter(description__icontains=my_filter_description)

    #     serializer = self.get_serializer(queryset, many = True)
    #     return Response(serializer.data)
    
class ColorsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'msg':'deleted'})

class SubCategoryViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'msg':'deleted'})

    @action(detail=False)
    def TopCategories(self,request):
        categories = SubCategory.objects.annotate(product_count=Count('product')).order_by('-product_count')[:3]
        serializer = SubCategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'msg':'deleted'})
