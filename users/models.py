import uuid
from django.contrib.auth.models import User

from django.db import models
from django.shortcuts import get_object_or_404
from django_extensions.db.models import TimeStampedModel


class UserAccount(TimeStampedModel):
    uuid = models.UUIDField('User ID', primary_key=True, default=uuid.uuid4)
    name = models.TextField('Name', max_length=512)
    description = models.TextField('Description', max_length=1000)
    email = models.EmailField('Email', max_length=1000)
    amount = models.FloatField('Max Amount')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def bitcoin_balance(self):
        return get_object_or_404(BitcoinCurrency,
                                 user_account=self.uuid).balance

    @property
    def ethereum_balance(self):
        return get_object_or_404(EthereumCurrency,
                                 user_account=self.uuid).balance


class Currency(TimeStampedModel):
    class Meta:
        abstract = True

    balance = models.FloatField('Bitcoin Wallet Balance',
                                max_length=1000000000)


class BitcoinCurrency(Currency):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE,
                                        related_name="bitcoin_currency")


class EthereumCurrency(Currency):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE,
                                        related_name="ethereum_currency")
