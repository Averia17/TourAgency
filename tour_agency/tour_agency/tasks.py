from celery import shared_task
from django.core.mail import send_mail

from tour_agency import settings


@shared_task
def test_task():
    print("The test task just ran.")


@shared_task
def send_ordered_tour_email(user_email, title):
    send_mail(
        "Order created",
        f"Thank you for ordering tour {title}",
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
