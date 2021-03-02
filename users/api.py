from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from users.models import UserAccount
from rest_framework.response import Response
from users.serializers import UserSerializer, UserAccountSerializer, \
    BitcoinCurrencySerializer, EthereumCurrencySerializer


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all().order_by('-created')

    def create(self, request, *args, **kwargs):
        request.data['email'] = request.data.get('email', None)
        request.data['username'] = request.data.get('email', None)
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        request.data['user'] = user_serializer.data['id']
        user_profile_serializer = self.serializer_class(data=request.data)
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()
        return Response(user_profile_serializer.data,
                        status=status.HTTP_201_CREATED)


class CurrencyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        get_object_or_404(UserAccount, uuid=kwargs['uuid'])
        if not request.data.get('type', None) or (request.data['type'] not in
                                                  ['bitcoin', 'ethereum']):
            return Response({'message': "You must choose Bitcoin or Ethereum "
                                        "currency"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.data['user_account'] = kwargs['uuid']
        if request.data['type'] == 'bitcoin':
            currency = BitcoinCurrencySerializer(data=request.data)
            currency.is_valid(raise_exception=True)
            currency.save()
        else:
            currency = EthereumCurrencySerializer(data=request.data)
            currency.is_valid(raise_exception=True)
            currency.save()
        return Response(currency.data, status=status.HTTP_201_CREATED)
