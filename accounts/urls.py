from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
# from .scheduler import start

# start()

router = DefaultRouter()

router.register("UserViewSet", views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    
]