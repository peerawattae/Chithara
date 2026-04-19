from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Offline, deterministic strategy for development and testing.
    Does not call any external API.
    Always returns a fixed placeholder result immediately.
    """

    PLACEHOLDER_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    PLACEHOLDER_DURATION = 120  # seconds

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Returns a predictable result based on the request.
        song_link is a fixed placeholder audio URL.
        task_id is a deterministic string based on the title so output is traceable in tests.
        """
        task_id = f"mock-{request.title.lower().replace(' ', '-')}"

        return GenerationResult(
            song_link=self.PLACEHOLDER_URL,
            duration=self.PLACEHOLDER_DURATION,
            raw_status="SUCCESS",
            task_id=task_id,
        )