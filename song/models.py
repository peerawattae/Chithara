from django.db import models
from library.models import Library
from song_form.models import SongForm
from creator.models import Creator


class GenerateStatus(models.TextChoices):
    """
    Enumeration Generate_status
    """
    IN_PROGRESS = "in_progress", "In Progress"
    SUCCESS     = "success",     "Success"
    FAILED      = "failed",      "Failed"


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
    song_link   = models.URLField(blank=True, null=True, unique=True,
                      help_text="Public share/stream link (Cloud Storage URL)")
    created_by  = models.CharField(max_length=150,
                      help_text="Name of the Creator who generated this song")
    duration    = models.IntegerField(default=0,
                      help_text="Duration in seconds")
    create_at   = models.DateTimeField(auto_now_add=True)
    cover_image = models.URLField(blank=True, null=True,
                      help_text="Cloud Storage URL; optional [0..1]")

    # Aggregation: Song can outlive its Library (song_link still valid)
    library     = models.ForeignKey(
                      Library,
                      on_delete=models.SET_NULL,
                      null=True, blank=True,
                      related_name="songs",
                  )

    # 1-to-1: Song has a SongForm
    song_form   = models.OneToOneField(
                      SongForm,
                      on_delete=models.PROTECT,   # Keep SongForm even if Song deleted
                      related_name="song",
                      null=True, blank=True,
                  )

    class Meta:
        app_label = "song"
        ordering = ["-create_at"]   # Diagram note: ordered by create_at descending

    def __str__(self):
        return f"{self.title} [{self.status}]"
