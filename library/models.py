from django.db import models
from creator.models import Creator


class Library(models.Model):
    """
    A personal collection belonging to one Creator.
    """
    owner = models.OneToOneField(
        Creator,
        on_delete=models.CASCADE,   # Composition: Library cannot exist without Creator
        related_name="library",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "library"
        verbose_name_plural = "libraries"

    def __str__(self):
        return f"Library of {self.owner.name}"
