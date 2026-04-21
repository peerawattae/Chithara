from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Offline, deterministic strategy for development and testing.
    Does not call any external API.
    Always returns a fixed placeholder result immediately.
    """

    PLACEHOLDER_DURATION = 120

    def generate(self, request: GenerationRequest) -> GenerationResult:
        task_id = f"mock-{request.title.lower().replace(' ', '-')}"

        # Make URL unique per task_id to avoid UNIQUE constraint on song_link
        song_link = f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3?task={task_id}"

        return GenerationResult(
            song_link=song_link,
            duration=self.PLACEHOLDER_DURATION,
            raw_status="SUCCESS",
            task_id=task_id,
        )