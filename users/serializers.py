from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar', 'first_name', 'last_name')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'