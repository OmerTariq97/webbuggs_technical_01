from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
# from .scheduler import start

# start()

router = DefaultRouter()

router.register("UserViewSet", views.UserViewSet)
router.register("ProductViewSet", views.ProductViewSet)
router.register("ColorsViewSet", views.ColorsViewSet)
router.register("SubCategoryViewSet", views.SubCategoryViewSet)
router.register("ProductCategoryViewSet", views.ProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    
]