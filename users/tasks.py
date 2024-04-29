from celery import shared_task

from users.services import block_users


@shared_task
def check_users():
    block_users()
