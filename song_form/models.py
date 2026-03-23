from django.db import models


class GenreChoices(models.TextChoices):
    """
    Enumeration from diagram: Genre
    Values: pop, hiphop, rock, reggae, country, R&B, EDM
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
    Diagram fields: occasion, genre (Genre enum), voice_type, mood, detail.
    1-to-1 with Song (has a relationship in diagram).
    Persists even if Song generation fails (A4).
    """
    occasion   = models.CharField(max_length=255)
    genre      = models.CharField(max_length=20, choices=GenreChoices.choices)
    voice_type = models.CharField(max_length=100)
    mood       = models.CharField(max_length=255)
    detail     = models.TextField(blank=True, default="")

    class Meta:
        app_label = "song_form"

    def __str__(self):
        return f"SongForm [{self.genre}] {self.occasion}"
