from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy


class AccountUserManager(BaseUserManager):
    def normalize_username(self, username):
        username = self.objects.normalize_email(username)
        return super().normalize_username(username)

    def _create_user(self, email, password, **extra_fields) -> 'AccountUser':
        """Create and save a user with the given email, and password."""
        if not email:
            msg = 'The given email must be set'
            raise ValueError(msg)
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,  # noqa: SLF001
            self.model._meta.object_name,  # noqa: SLF001
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            msg = 'Superuser must have is_staff=True.'
            raise ValueError(msg)
        if extra_fields.get('is_superuser') is not True:
            msg = 'Superuser must have is_superuser=True.'
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)


class AccountUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        gettext_lazy('email'),
        unique=True,
        max_length=settings.LONG_LENGTH_CHARFIELD,
        help_text=gettext_lazy('Required. Unique. Letters, digits and ".", "_", "-".'),
        error_messages={
            'unique': gettext_lazy('A user with that email already exists.'),
        },
    )
    first_name = models.CharField(
        gettext_lazy('first name'),
        blank=True,
        max_length=settings.SHORT_LENGTH_CHARFIELD,
        help_text=gettext_lazy('Only letters an digits.'),
    )
    last_name = models.CharField(
        gettext_lazy('last name'),
        blank=True,
        max_length=settings.SHORT_LENGTH_CHARFIELD,
        help_text=gettext_lazy('Only letters an digits.'),
    )
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default=False,
        help_text=gettext_lazy('Designates whether this user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=False,
        help_text=gettext_lazy('Designates whether this user should be threated as active.'),
    )
    date_joined = models.DateTimeField(
        gettext_lazy('date joined'),
        auto_now_add=True,
    )

    objects = AccountUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = gettext_lazy('user')
        verbose_name_plural = gettext_lazy('users')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
