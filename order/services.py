from django.db import transaction
from decimal import Decimal

class CryptoService:
    def __init__(self, user_service, crypto_repository, order_repository, event_log_repository):
        self.user_service = user_service
        self.crypto_repository = crypto_repository
        self.order_repository = order_repository
        self.event_log_repository = event_log_repository

    def purchase_crypto(self, user, crypto_name, amount):
        cryptocurrency = self.crypto_repository.get_crypto_by_name(crypto_name)
        total_price = cryptocurrency.price * amount

        with transaction.atomic():
            user = self.user_service.get_user_with_lock(user.id)
            if user.wallet.balance < total_price:
                raise Exception('Insufficient balance')

            user.wallet.balance -= total_price
            user.wallet.save()

            order = self.order_repository.create_order(user, cryptocurrency, amount, total_price)
            self.event_log_repository.create_log(user, order, 'DEDUCTION', total_price)

            return order