from celery import shared_task
from django.core.mail import EmailMessage

from core.constants import ORDER_FILE_PATH
from tour_agency import settings


@shared_task
def test_task():
    print("The test task just ran.")


@shared_task
def send_ordered_tour_email(user_email, subject, message, attach_file=False):
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_email])
    if attach_file:
        file = open(ORDER_FILE_PATH, "r", errors="ignore")
        mail.attach("OrderRequest.pdf", file.read(), "application/pdf")
    mail.send()
