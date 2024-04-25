import os

import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')


def create_stripe_product_with_price(product_name, price):
    product = stripe.Product.create(name=product_name, default_price_data=
                                    {
                                        'currency': 'rub',
                                        'unit_amount': price * 100
                                    }
                                    )
    return product.get('default_price')


def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def get_stripe_payment_status(payment_id):
    session = stripe.checkout.Session.retrieve(payment_id)
    return session.get('payment_status')
