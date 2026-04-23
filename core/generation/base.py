from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GenerationRequest:
    """
    Data passed into any song generator strategy.
    Maps directly from SongForm fields.
    """
    title: str
    occasion: str
    genre: str
    voice_type: str
    mood: str
    detail: str = ""


@dataclass
class GenerationResult:
    """
    Data returned by any song generator strategy.
    Used to update the Song record after generation.
    """
    song_link: str        # URL to the generated audio file
    duration: int         # Duration in seconds
    raw_status: str       # Status string returned by the strategy (e.g. "SUCCESS")
    task_id: str = ""     # Optional: external task ID (used by Suno, empty for Mock)
    cover_image: str = "" # Optional: cover image URL returned by the strategy


class SongGeneratorStrategy(ABC):
    """
    Abstract base class for all song generation strategies.
    Any new strategy (Mock, Suno, etc.) must implement generate().
    """

    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate a song from the given request.
        Returns a GenerationResult on success.
        """
        ...