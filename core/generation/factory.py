from django.conf import settings
from .base import SongGeneratorStrategy
from .mock import MockSongGeneratorStrategy


def get_generator() -> SongGeneratorStrategy:
    """
    Central factory — returns the active strategy based on
    the GENERATOR_STRATEGY Django setting.

    "mock" → MockSongGeneratorStrategy  (default, offline)
    "suno" → SunoSongGeneratorStrategy  (Phase 4, real API)

    Never use if/else outside this function to pick a strategy.
    """
    strategy = getattr(settings, "GENERATOR_STRATEGY", "mock")

    if strategy == "suno":
        # Imported here to avoid loading Suno dependencies in mock mode
        from .suno import SunoSongGeneratorStrategy
        return SunoSongGeneratorStrategy()

    return MockSongGeneratorStrategy()