from django.db import models


# Enumerations
class GenreChoices(models.TextChoices):
    POP     = "pop",     "Pop"
    HIPHOP  = "hiphop",  "Hip-Hop"
    ROCK    = "rock",    "Rock"
    REGGAE  = "reggae",  "Reggae"
    COUNTRY = "country", "Country"
    RNB     = "rnb",     "R&B"
    EDM     = "edm",     "EDM"


class GenerateStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "In Progress"
    SUCCESS     = "success",     "Success"
    FAILED      = "failed",      "Failed"


# User
class User(models.Model):
    """
    Base class for all users. Authentication via Google OAuth.
    """
    name            = models.CharField(max_length=150)
    google_oauth_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "core"

    def __str__(self):
        return self.name



# Creator  (inherits User — multi-table inheritance)
class Creator(User):
    """
    A User who generates music.
    """
    quota = models.IntegerField(default=20)

    class Meta:
        app_label = "core"

    def __str__(self):
        return f"Creator({self.name})"


# ─────────────────────────────────────────────
# Listener  (inherits User — multi-table inheritance)
# ─────────────────────────────────────────────

class Listener(User):
    """
    A User whose main interest is listening to shared songs.
    A User can be both a Creator and a Listener simultaneously.
    """

    class Meta:
        app_label = "core"

    def __str__(self):
        return f"Listener({self.name})"



# Library  (composition with Creator)
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


# SongForm  (input submitted by Creator)
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


# Song  (output from AI generation)
class Song(models.Model):
    """
    The generated audio track from AI.
    """
    title       = models.CharField(max_length=255)
    status      = models.CharField(
                      max_length=20,
                      choices=GenerateStatus.choices,
                      default=GenerateStatus.IN_PROGRESS,
                  )
    song_link   = models.URLField(
                      blank=True, null=True, unique=True,
                      help_text="Auto-set after successful AI generation. Never entered by user.",
                  )
    created_by  = models.CharField(max_length=150,
                      help_text="Name of the Creator who generated this song")
    duration    = models.IntegerField(default=0,
                      help_text="Duration in seconds")
    create_at   = models.DateTimeField(auto_now_add=True)
    cover_image = models.URLField(blank=True, null=True,
                      help_text="Optional cover image URL [0..1]")

    # Aggregation: Song outlives its Library
    library     = models.ForeignKey(
                      Library,
                      on_delete=models.SET_NULL,  # Aggregation
                      null=True, blank=True,
                      related_name="songs",
                  )

    # 1-to-1: every Song was created from exactly one SongForm
    song_form   = models.OneToOneField(
                      SongForm,
                      on_delete=models.PROTECT,   # SongForm must not be deleted while Song exists
                      related_name="song",
                      null=True, blank=True,
                  )

    class Meta:
        app_label = "core"
        ordering  = ["-create_at"]  # diagram note: ordered by create_at descending

    def __str__(self):
        return f"{self.title} [{self.status}]"
