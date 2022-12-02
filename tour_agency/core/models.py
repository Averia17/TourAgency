from django.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class ImageUploadMixin:
    def perform_create(self, serializer):
        serializer.save(images=self.request.FILES.getlist("images"))

    def perform_update(self, serializer):
        serializer.save(images=self.request.FILES.getlist("images"))
