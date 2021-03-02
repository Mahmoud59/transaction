from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.api import UserViewSet, CurrencyAPIView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('users/<str:uuid>/currency/', CurrencyAPIView.as_view(),
         name="users-currency")
]

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns += router.urls
