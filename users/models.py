from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):

    PAYMENT_CHOICES = {
        'cash': 'наличными',
        'card': 'по карте'
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course_subject = models.ForeignKey(Course, on_delete=models.SET_NULL,
                                       related_name='payments', **NULLABLE)
    lesson_subject = models.ForeignKey(Lesson, on_delete=models.SET_NULL,
                                       related_name='payments', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(choices=PAYMENT_CHOICES, verbose_name='способ оплаты')
    session_id = models.CharField(max_length=255, verbose_name='id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='ссылка на оплату', **NULLABLE)

    def __str__(self):
        if self.course_subject:
            subject = f'курс {self.course_subject}'
        else:
            subject = f'урок {self.lesson_subject}'
        return f"{self.amount} рублей от {self.date} за {subject}"

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
