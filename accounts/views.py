from rest_framework import viewsets
from .models import User
from products.models import Product
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail = False)
    def ProductUploads(self, request):
        user = self.request.query_params.get('user')
        queryset = Product.objects.filter(created_by = user)
        Uploads = queryset.count()
        # instance = User.objects.get(id=user)
        try:
            user = User.objects.get(id=user)
        except User.DoesNotExist:
            return Response({'No such user'})
        else:
            if queryset:
                return Response({f'User {user} has {Uploads} Product Uploads'})
            else:
                return Response({f'{user} has 0 uploads'})

      
class LoginView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [AllowAny]
    # @csrf_protect
    def post(self, request, format = None):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            account = User.objects.get(email = email)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})
        user = authenticate(request=request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'})

        token, _ = Token.objects.get_or_create(user=user)
        if account:
            if account.is_active:
                login(request, account, backend="django.contrib.auth.backends.ModelBackend")

                Res = {"token": token.key}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
        
class LogoutView(APIView):

    def get(self, request, format = None):
        request.user.auth_token.delete()

        logout(request)

        return Response('User Logged out successfully')