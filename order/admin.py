from django.contrib import admin
from .models import Cryptocurrency, Wallet, Order, EventLog

admin.site.register(Cryptocurrency)
admin.site.register(Wallet)
admin.site.register(Order)
admin.site.register(EventLog)