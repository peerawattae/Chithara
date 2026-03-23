from django.db import models


class User(models.Model):
    """
    Base class for all users. Authentication via Google OAuth.
    """
    name = models.CharField(max_length=150)
    google_oauth_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "user"

    def __str__(self):
        return self.name
