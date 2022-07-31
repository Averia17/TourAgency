from django.utils import timezone
import ast

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from core.constants import CHECK_IN_TIME


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


# will be deleting from AWS
def delete_image(image):
    image.delete()


def string_to_list(string):
    if not isinstance(string, str):
        return string
    if len(string) == 1:
        string = str([string])
    return ast.literal_eval(string)


def string_to_datetime(date):
    date = f"{date} {CHECK_IN_TIME}"
    return make_aware(parse_datetime(date))


def true(value: str) -> bool:
    return value in [True, "true", "True", "1"]
