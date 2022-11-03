import logging.config
from datetime import timedelta

from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone

from core.constants import NUMBER_BOOKED_DAYS
from tour_agency import settings
from orders.models import Order

logger = logging.getLogger(__name__)


@shared_task
def test_task():
    print("The test task just ran.")


@shared_task
def send_ordered_tour_email(user_email, subject, message, file_path=""):
    logger.info("start send email task")
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_email])
    if file_path:
        with open(file_path, "r", errors="ignore") as file:
            mail.attach(file.name, file.read(), "application/pdf")
    mail.send()
    logger.info("email sent to %s", user_email)


# CELERY_BEAT_SCHEDULE_TASKS
@shared_task
def check_expire_booked_order():
    logger.info("start expire book orders check task")
    end_booked_time = timezone.now() - timedelta(days=NUMBER_BOOKED_DAYS)
    deleted_orders, count_deleted = Order.objects.filter(
        created__lte=end_booked_time, status="BOOKED"
    ).delete()
    logger.info("deleted orders count %s", count_deleted.get("orders.Order", 0))


@shared_task
def check_booked_time():
    logger.info("start book time check task")
    end_booked_time = timezone.now() - timedelta(days=NUMBER_BOOKED_DAYS, hours=-3)
    orders = Order.objects.filter(created__lte=end_booked_time, status="BOOKED")
    for order in orders:
        send_ordered_tour_email.delay(
            order.user.email,
            "Booking Order",
            f"Booking time for your order №{order.id} expires in less than 3 hours",
        )
