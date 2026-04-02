from .user import User


class Listener(User):
    """
    A User whose main interest is listening to shared songs.
    A User can be both a Creator and a Listener simultaneously.
    """

    class Meta:
        app_label = "core"

    def __str__(self):
        return f"Listener({self.name})"
