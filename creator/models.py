from django.db import models
from user.models import User


class Creator(User):
    """
    A User whose main interest is creating/generating music.
    Inherits from User.
    """
    quota = models.IntegerField(default=20, help_text="Remaining generations today (max 20/day)")

    class Meta:
        app_label = "creator"

    def __str__(self):
        return f"Creator({self.name})"
