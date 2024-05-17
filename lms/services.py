from django.core.mail import send_mail
from django.conf import settings


def send_update_email(recipients, course_name):
    """Отправка e-mail об обновлениях в курсе"""
    send_mail(
        'Изменения в курсе',
        f'В курсе {course_name} произошли изменения.\n'
        'Проверьте на сайте',
        settings.EMAIL_HOST_USER,
        recipients,
        fail_silently=True
    )
