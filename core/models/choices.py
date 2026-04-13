from django.db import models


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
