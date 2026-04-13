from django.db import models

from .creator import Creator


class Library(models.Model):
    """
    Personal song collection belonging to one Creator.
    """
    owner      = models.OneToOneField(
                     Creator,
                     on_delete=models.CASCADE,  # Composition
                     related_name="library",
                 )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "core"
        verbose_name_plural = "libraries"

    def __str__(self):
        return f"Library of {self.owner.name}"
