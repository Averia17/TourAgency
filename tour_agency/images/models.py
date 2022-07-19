from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from core.utils import delete_image
from hotels.models import Hotel, RoomType
from locations.models import Country
from tours.models import Tour
from users.models import User

from images.AWS import settings
from images.utils import image_generate_upload_path


class ImageManager(models.QuerySet):
    def delete(self):
        for obj in self:
            delete_image(obj.image)
        return super().delete()


class Image(BaseModel):
    image = models.ImageField(
        _("Image"),
        upload_to=image_generate_upload_path,
    )

    original_file_name = models.TextField()
    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    objects = ImageManager.as_manager()

    def __str__(self):
        return self.original_file_name

    class Meta:
        app_label = "images"
        verbose_name_plural = "Images"

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == "s3":
            return self.image.url

        return f"{settings.APP_DOMAIN}{self.image.url}"

    def delete(self, using=None, keep_parents=False):
        delete_image(self.image)
        return super().delete(using, keep_parents)


class HotelImage(Image):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")

    class Meta(Image.Meta):
        verbose_name_plural = "HotelImages"


class RoomImage(Image):
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="images")

    class Meta(Image.Meta):
        verbose_name_plural = "RoomImages"


class TourImage(Image):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="images")

    class Meta(Image.Meta):
        verbose_name_plural = "TourImages"


class CountryImage(Image):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="images"
    )

    class Meta(Image.Meta):
        verbose_name_plural = "CountryImages"
