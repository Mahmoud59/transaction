from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
import uuid as uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from rest_framework.exceptions import ValidationError

from users.models import UserAccount


class Transaction(TimeStampedModel):
    class StateType(models.TextChoices):
        PENDING = 'pending', _('pending')
        SUCCESS = 'success', _('success')
        FAILED = 'failed', _('failed')

    class CurrencyType(models.TextChoices):
        BITCOIN = 'bitcoin', _('bitcoin')
        ETHEREUM = 'ethereum', _('ethereum')

    uuid = models.UUIDField('User ID', primary_key=True, default=uuid.uuid4)
    currency_amount = models.FloatField('Currency Amount')
    currency_type = models.CharField('Currency Type', max_length=8,
                                     choices=CurrencyType.choices)
    sender_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                    related_name="sender_user")
    receiver_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                      related_name="receiver_user")
    state = models.TextField('State', max_length=7, choices=StateType.choices,
                             default=StateType.PENDING)

    def save(self, **kwargs):
        sender_user = get_object_or_404(UserAccount,
                                        uuid=self.sender_user.uuid)
        if self.sender_user == self.receiver_user:
            raise ValidationError("Sender can't be receiver in the same "
                                  "transaction.")
        elif sender_user.amount < self.currency_amount:
            raise ValidationError("Sender amount for transactions is less than"
                                  " this transaction amount.")
        elif self.currency_type == self.CurrencyType.BITCOIN:
            if self.currency_amount > sender_user.bitcoin_currency.balance:
                raise ValidationError("Sender bitcoin amount not enough.")
            else:
                sender_currency = sender_user.bitcoin_currency
                sender_currency.balance -= self.currency_amount
                sender_currency.save()
        elif self.currency_type == self.CurrencyType.ETHEREUM:
            if self.currency_amount > sender_user.ethereum_currency.balance:
                raise ValidationError("Sender ethereum amount not enough.")
            else:
                sender_currency = sender_user.ethereum_currency
                sender_currency.balance -= self.currency_amount
                sender_currency.save()
        else:
            super().save(**kwargs)

