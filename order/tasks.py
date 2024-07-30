from celery import shared_task
from .models import Order, Cryptocurrency
from .views import OrderViewSet
from decimal import Decimal

@shared_task
def check_and_combine_orders():
    cryptocurrencies = Cryptocurrency.objects.all()
    for cryptocurrency in cryptocurrencies:
        orders = Order.objects.filter(cryptocurrency=cryptocurrency, combined=False)
        total_price = sum(order.total_price for order in orders)

        if total_price < Decimal('10.00'):
            continue

        total_amount = sum(order.amount for order in orders)
        OrderViewSet().buy_from_exchange(cryptocurrency, total_amount)
        orders.update(combined=True)