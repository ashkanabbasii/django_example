from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cryptocurrency, Order, EventLog, Wallet
from .services import CryptoService
from .repositories import UserRepository, CryptoRepository, OrderRepository, EventLogRepository
from decimal import Decimal

class OrderTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='pass')
        self.user2 = User.objects.create(username='user2', password='pass')
        self.user3 = User.objects.create(username='user3', password='pass')
        self.crypto = Cryptocurrency.objects.create(name='ABAN', price=4)

        Wallet.objects.create(user=self.user1, balance=100)
        Wallet.objects.create(user=self.user2, balance=100)
        Wallet.objects.create(user=self.user3, balance=100)

        self.user_repository = UserRepository()
        self.crypto_repository = CryptoRepository()
        self.order_repository = OrderRepository()
        self.event_log_repository = EventLogRepository()

        self.crypto_service = CryptoService(self.user_repository, self.crypto_repository, self.order_repository, self.event_log_repository)

    def test_large_order(self):
        order = self.crypto_service.purchase_crypto(self.user1, 'ABAN', Decimal('3'))
        self.assertEqual(order.total_price, 12)
        self.assertEqual(self.user1.wallet.balance, 88)
        self.assertTrue(Order.objects.filter(id=order.id).exists())

    def test_multiple_small_orders(self):
        self.crypto_service.purchase_crypto(self.user1, 'ABAN', Decimal('1'))
        self.crypto_service.purchase_crypto(self.user2, 'ABAN', Decimal('1'))
        self.crypto_service.purchase_crypto(self.user3, 'ABAN', Decimal('1'))

        self.assertEqual(self.user1.wallet.balance, 96)
        self.assertEqual(self.user2.wallet.balance, 96)
        self.assertEqual(self.user3.wallet.balance, 96)

        small_orders = Order.objects.filter(cryptocurrency=self.crypto, combined=False)
        self.assertEqual(small_orders.count(), 3)

        check_and_combine_orders()

        combined_orders = Order.objects.filter(cryptocurrency=self.crypto, combined=True)
        self.assertEqual(combined_orders.count(), 3)