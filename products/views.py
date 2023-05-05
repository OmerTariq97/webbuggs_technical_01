from django.shortcuts import render
from .models import Product, Colors, SubCategory
from .serializers import ProductSerializer, ColorsSerializer, SubCategorySerializer
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ColorsViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer

@method_decorator(csrf_exempt, name='dispatch')
class SubCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class LoginView(APIView):
    permission_classes=[AllowAny]

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
    # permission_classes = [IsAuthenticated]

    def post(self, request, format = None):
        print(request.user)
        request.user.auth_token.delete()

        logout(request)

        return Response('User Logged out successfully')