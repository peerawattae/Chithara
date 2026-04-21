from django.conf import settings
from .base import SongGeneratorStrategy
from .mock import MockSongGeneratorStrategy


def get_generator() -> SongGeneratorStrategy:
    """
    Central factory — returns the active strategy based on
    the GENERATOR_STRATEGY Django setting.

    "mock" → MockSongGeneratorStrategy
    "suno" → SunoSongGeneratorStrategy

    """
    strategy = getattr(settings, "GENERATOR_STRATEGY", "mock")

    if strategy == "suno":
        # Imported here to avoid loading Suno dependencies in mock mode
        from .suno import SunoSongGeneratorStrategy
        return SunoSongGeneratorStrategy()

    return MockSongGeneratorStrategy()