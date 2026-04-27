from django.db import models

from .choices import GenerateStatus
from .library import Library
from .song_form import SongForm


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
    is_shared = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True, help_text="Set if generation fails")

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