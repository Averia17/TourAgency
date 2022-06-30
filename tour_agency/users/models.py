from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


from core.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("The email must be set")
        if not password:
            raise ValueError("The password must be set")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(_("Email"), unique=True, max_length=256, blank=False)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_active = models.BooleanField(_("Is active"), default=True)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        app_label = "users"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.pk}: {self.email}"

    def has_module_perms(self, app_label):
        return self.is_staff and self.is_active

    def has_perm(self, perm_list, obj=None):
        return self.is_staff and self.is_active
