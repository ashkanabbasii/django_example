from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import CryptoService
from .repositories import UserRepository, CryptoRepository, OrderRepository, EventLogRepository
from .serializers import OrderSerializer
from decimal import Decimal
import requests

user_repository = UserRepository()
crypto_repository = CryptoRepository()
order_repository = OrderRepository()
event_log_repository = EventLogRepository()

crypto_service = CryptoService(user_repository, crypto_repository, order_repository, event_log_repository)

class OrderViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        crypto_name = request.data.get('cryptocurrency')
        amount = Decimal(request.data.get('amount'))

        try:
            order = crypto_service.purchase_crypto(user, crypto_name, amount)
            self.combine_small_orders(order.cryptocurrency)
            return Response(OrderSerializer(order).data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def combine_small_orders(self, cryptocurrency):
        threshold = Decimal('10.00')
        small_orders = Order.objects.filter(
            cryptocurrency=cryptocurrency,
            combined=False
        )
        total_amount = sum(order.amount for order in small_orders)
        total_price = sum(order.total_price for order in small_orders)

        if total_price >= threshold:
            self.buy_from_exchange(cryptocurrency, total_amount)
            small_orders.update(combined=True)

    def buy_from_exchange(self, cryptocurrency, amount):
        url = "http://exchange.com/api/buy"
        data = {
            "cryptocurrency": cryptocurrency.name,
            "amount": amount
        }
        response = requests.post(url, json=data)
        return response.json()