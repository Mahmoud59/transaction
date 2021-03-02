from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from users.models import UserAccount


class TransactionViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().order_by('-created')

    def create(self, request, *args, **kwargs):
        request.data['sender_user'] = get_object_or_404(
            UserAccount, user=request.user.id).uuid
        transaction = self.serializer_class(data=request.data)
        transaction.is_valid(raise_exception=True)
        transaction.save()
        return Response(transaction.data, status=status.HTTP_201_CREATED)


class UserTransactionViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get(self, request, user_uuid):
        get_object_or_404(UserAccount, uuid=user_uuid)
        user_transactions = Transaction.objects.filter(
            Q(sender_user=user_uuid) | Q(receiver_user=user_uuid))
        user_transactions_serializer = self.serializer_class(
            user_transactions, many=True)
        return Response(user_transactions_serializer.data,
                        status=status.HTTP_200_OK)
