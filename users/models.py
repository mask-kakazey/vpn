from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Повне ім'я"),
                            null=True, blank=True)
    email = models.EmailField(unique=True, max_length=180)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        # unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        unique=False,
        null=True,
    )
