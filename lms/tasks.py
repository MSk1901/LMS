from celery import shared_task

from lms.services import send_update_email


@shared_task
def update_course(recipients, course_name):
    send_update_email(recipients, course_name)
