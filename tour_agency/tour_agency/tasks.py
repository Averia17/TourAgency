import logging.config
from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMessage

from core.constants import ORDER_FILE_PATH, NUMBER_BOOKED_DAYS, ORDER_FILE_NAME
from tour_agency import settings
from orders.models import Order

logger = logging.getLogger(__name__)


@shared_task
def test_task():
    print("The test task just ran.")


@shared_task
def send_ordered_tour_email(user_email, subject, message, attach_file=False):
    logger.info("start send email task")
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_email])
    if attach_file:
        file = open(ORDER_FILE_PATH, "r", errors="ignore")
        mail.attach(ORDER_FILE_NAME, file.read(), "application/pdf")
    mail.send()
    logger.info("email sent to %s", user_email)


# CELERY_BEAT_SCHEDULE_TASKS
@shared_task
def check_booked_time():
    logger.info("start book time check task")
    end_booked_time = datetime.now() - timedelta(days=NUMBER_BOOKED_DAYS)
    deleted_orders, count_deleted = Order.objects.filter(
        created__lte=end_booked_time
    ).delete()
    logger.info("deleted orders count %s", count_deleted.get("orders.Order", 0))
