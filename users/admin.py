from django.contrib import admin

from users.models import UserAccount, BitcoinCurrency, EthereumCurrency


admin.site.register(UserAccount)
admin.site.register(BitcoinCurrency)
admin.site.register(EthereumCurrency)
