from django.db import models

from .choices import GenreChoices
from .creator import Creator


class SongForm(models.Model):
    """
    Input form submitted by a Creator to generate a Song.
    """
    creator    = models.ForeignKey(
                     Creator,
                     on_delete=models.CASCADE,
                     related_name="song_forms",
                     help_text="Auto-assigned when user becomes a Creator on first submission",
                 )
    occasion   = models.CharField(max_length=255)
    genre      = models.CharField(max_length=20, choices=GenreChoices.choices)
    voice_type = models.CharField(max_length=100)
    mood       = models.CharField(max_length=255)
    detail     = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "core"
        ordering  = ["-created_at"]

    def __str__(self):
        return f"SongForm [{self.genre}] {self.occasion} by {self.creator.name}"
