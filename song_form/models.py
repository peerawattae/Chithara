from django.db import models
from creator.models import Creator

class GenreChoices(models.TextChoices):
    """
    Enumerate class Genre
    """
    POP     = "pop",     "Pop"
    HIPHOP  = "hiphop",  "Hip-Hop"
    ROCK    = "rock",    "Rock"
    REGGAE  = "reggae",  "Reggae"
    COUNTRY = "country", "Country"
    RNB     = "rnb",     "R&B"
    EDM     = "edm",     "EDM"


class SongForm(models.Model):
    """
    Input form used by a Creator to generate a Song.
    """

    creator    = models.ForeignKey(
                     Creator,
                     on_delete=models.CASCADE,
                     related_name="song_forms"
                 )
    occasion   = models.CharField(max_length=255)
    genre      = models.CharField(max_length=20, choices=GenreChoices.choices)
    voice_type = models.CharField(max_length=100)
    mood       = models.CharField(max_length=255)
    detail     = models.TextField(blank=True, default="")

    class Meta:
        app_label = "song_form"

    def __str__(self):
        return f"SongForm [{self.genre}] {self.occasion}"
