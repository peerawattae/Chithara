from django.db import models
from user.models import User


class Listener(User):
    """
    A User whose main interest is listening to shared songs.
    """

    class Meta:
        app_label = "listener"

    def __str__(self):
        return f"Listener({self.name})"
