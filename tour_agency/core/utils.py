from django.utils import timezone
import ast


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


# will be deleting from AWS
def delete_image(image):
    image.delete()


def string_to_list(string):
    if not isinstance(string, str):
        return string
    return ast.literal_eval(string)
