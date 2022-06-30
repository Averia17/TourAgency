import mimetypes
from typing import Tuple

from django.core.exceptions import ValidationError
from django.db import transaction

from images.AWS import settings
from images.models import Image
from images.utils import file_generate_name, bytes_to_mib
from users.models import User


def _validate_file_size(file_obj):
    max_size = settings.FILE_MAX_SIZE

    if file_obj.size > max_size:
        raise ValidationError(
            f"File is too large. It should not exceed {bytes_to_mib(max_size)} MiB"
        )


class FileStandardUploadService:
    def __init__(self, model, user: User):
        self.model = model
        self.user = user

    def _infer_file_name_and_type(
        self, file, file_name: str = "", file_type: str = ""
    ) -> Tuple[str, str]:
        if not file_name:
            file_name = file.name

        if not file_type:
            guessed_file_type, encoding = mimetypes.guess_type(file_name)

            if guessed_file_type is None:
                file_type = ""
            else:
                file_type = guessed_file_type

        return file_name, file_type

    @transaction.atomic
    def create(self, file, file_name: str = "", file_type: str = "", **kwargs) -> Image:
        _validate_file_size(file)

        file_name, file_type = self._infer_file_name_and_type(
            file, file_name, file_type
        )

        obj = self.model(
            image=file,
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            **kwargs,
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def update(
        self,
        instance: Image,
        file,
        image_name: str = "",
        image_type: str = "",
        **kwargs,
    ) -> Image:
        _validate_file_size(file)

        image_name, image_type = self._infer_file_name_and_type(
            file, image_name, image_type
        )
        obj_fields = {
            "image": file,
            "original_file_name": image_name,
            "file_name": file_generate_name(image_name),
            "file_type": image_type,
            "uploaded_by": self.user,
            **kwargs,
        }
        instance.__dict__.update(obj_fields)

        instance.full_clean()
        instance.save()

        return instance
