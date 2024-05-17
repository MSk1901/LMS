from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_product_with_price, create_stripe_session


class PaymentListAPIView(generics.ListAPIView):
    """Представление для просмотра списка платежей"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_subject', 'lesson_subject', 'method')
    ordering_fields = ['date']


class PaymentCreateAPIView(generics.CreateAPIView):
    """Представление для создания платежа"""
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.course_subject:
            product = payment.course_subject
        elif payment.lesson_subject:
            product = payment.lesson_subject
        else:
            error_message = {
                "course_subject": [
                    "One of these fields is required."
                ],
                "lesson_subject": [
                    "One of these fields is required."
                ]
            }
            raise serializers.ValidationError(error_message)
        if payment.method == 'card':
            stripe_price = create_stripe_product_with_price(product.title, payment.amount)
            session_id, payment_link = create_stripe_session(stripe_price)
            payment.session_id = session_id
            payment.link = payment_link
        payment.save()


class UserViewSet(viewsets.ModelViewSet):
    """Вью сет для пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
