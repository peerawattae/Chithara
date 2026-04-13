from django.db import models

from .user import User


class Creator(User):
    """
    A User who generates music.
    """
    quota = models.IntegerField(default=20)

    class Meta:
        app_label = "core"

    def __str__(self):
        return f"Creator({self.name})"
