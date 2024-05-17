from celery import shared_task

from users.services import block_users


@shared_task
def check_users():
    """Таск celery для блокировки пользователей"""
    block_users()
