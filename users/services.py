import os
from datetime import timedelta

import stripe

from django.utils import timezone

from users.models import User

stripe.api_key = os.getenv('STRIPE_API_KEY')


def create_stripe_product_with_price(product_name, price):
    """Создание продукта Stripe с ценой"""
    product = stripe.Product.create(
        name=product_name,
        default_price_data={
            'currency': 'rub',
            'unit_amount': price * 100
        }
    )
    return product.get('default_price')


def create_stripe_session(price_id):
    """Создание сессии Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def get_stripe_payment_status(payment_id):
    """Получение статуса оплаты в Stripe"""
    session = stripe.checkout.Session.retrieve(payment_id)
    return session.get('payment_status')


def block_users():
    """Блокировка неактивных пользователей"""
    users = User.objects.exclude(last_login__isnull=True)
    now = timezone.now()
    for user in users:
        if now - user.last_login > timedelta(days=31):
            user.is_active = False
            user.save()
