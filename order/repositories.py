from django.db import transaction
from django.contrib.auth.models import User
from .models import Order, Cryptocurrency, EventLog

class UserRepository:
    def get_user_with_lock(self, user_id):
        user = User.objects.select_for_update().get(id=user_id)
        return user

class CryptoRepository:
    def get_crypto_by_name(self, name):
        return Cryptocurrency.objects.get(name=name)

class OrderRepository:
    def create_order(self, user, cryptocurrency, amount, total_price):
        return Order.objects.create(
            user=user,
            cryptocurrency=cryptocurrency,
            amount=amount,
            total_price=total_price
        )

class EventLogRepository:
    def create_log(self, user, order, action, amount):
        return EventLog.objects.create(
            user=user,
            order=order,
            action=action,
            amount=amount
        )