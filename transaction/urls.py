from django.urls import path
from rest_framework.routers import DefaultRouter

from transaction.api import TransactionViewSet, UserTransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
urlpatterns = router.urls

urlpatterns += [
    path('users/<str:user_uuid>/transactions/',
         UserTransactionViewSet.as_view(), name="user-transactions")
]
