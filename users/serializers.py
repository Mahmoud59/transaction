from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import UserAccount, BitcoinCurrency, EthereumCurrency


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        """Hash the password correctly."""
        return make_password(password)


class UserAccountSerializer(serializers.ModelSerializer):
    bitcoin_balance = serializers.ReadOnlyField()
    ethereum_balance = serializers.ReadOnlyField()

    class Meta:
        model = UserAccount
        fields = '__all__'


class BitcoinCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinCurrency
        fields = '__all__'


class EthereumCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = EthereumCurrency
        fields = '__all__'
