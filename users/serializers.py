from rest_framework import serializers

from users.models import User, Payment
from users.services import get_stripe_payment_status


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payment"""
    status = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'date', 'session_id', 'link')

    def get_status(self, instance):
        """Проверка статуса оплаты"""
        if instance.session_id:
            return get_stripe_payment_status(instance.session_id)
        return None
