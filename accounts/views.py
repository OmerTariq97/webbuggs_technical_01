from rest_framework import viewsets
from .models import User
from products.models import Product, Colors, SubCategory, ProductCategory
from products.serializers import ProductSerializer, ColorsSerializer, SubCategorySerializer, ProductCategorySerializer, TopCategoriesSerializer
from .serializers import UserSerializer,LoginSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from django.core.exceptions import ValidationError
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail = False)
    def ProductUploads(self, request):
        user = self.request.query_params.get('user')
        queryset = Product.objects.filter(created_by = user)
        Uploads = queryset.count()
        if queryset:
            return Response({f'User {User.objects.get(id=user).email} has {Uploads} Product Uploads'})
        else:
            return Response({'No such user'})
@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'msg':'deleted'})

    @action(detail=False, methods=['get'])
    def filter(self, request):
        my_filter_SKU = self.request.query_params.get('filter_SKU')
        my_filter_title = self.request.query_params.get('filter_title')
        my_filter_description = self.request.query_params.get('filter_description')

        queryset = self.get_queryset()
        if my_filter_SKU:
            queryset = queryset.filter(sku__icontains=my_filter_SKU)
        elif my_filter_title:
            queryset = queryset.filter(title__icontains=my_filter_title)
        elif my_filter_description:
            queryset = queryset.filter(description__icontains=my_filter_description)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
    
@method_decorator(csrf_exempt, name='dispatch')
class ColorsViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'msg':'deleted'})

@method_decorator(csrf_exempt, name='dispatch')
class SubCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
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

# class TopCategoriesViewSet(viewsets.ModelViewSet):
#     queryset = SubCategory.objects.all()
#     serializer_class = TopCategoriesSerializer

#     def get_queryset(self):
#         return SubCategory.objects.annotate(product_count=Count('product')).order_by('-product_count')[:3]
# @method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [AllowAny]
    # @csrf_protect
    def post(self, request, format = None):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            Account = User.objects.get(email = email)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})
        user = authenticate(request=request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'})

        token, _ = Token.objects.get_or_create(user=user)
        if Account:
            if Account.is_active:
                login(request, Account)

                Res = {"token": token.key}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
        
class LogoutView(APIView):

    def get(self, request, format = None):
        print(request.user.auth_token)
        request.user.auth_token.delete()

        logout(request)

        return Response('User Logged out successfully')

# from .tasks import testfunc

# def test(request):
#     testfunc.delay()
#     return HttpResponse('Done')