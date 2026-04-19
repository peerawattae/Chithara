import time
import requests
from django.conf import settings

from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Calls the Suno API at api.sunoapi.org.
    Requires SUNO_API_KEY in environment / Django settings.

    Flow:
      POST /api/v1/generate      → get taskId
      GET  /api/v1/generate/record-info  → poll until SUCCESS
    """

    BASE_URL    = "https://api.sunoapi.org"
    POLL_INTERVAL  = 15   # seconds between each status check
    MAX_ATTEMPTS   = 40   # 40 × 15s = 10 minutes max wait

    # Suno status values
    TERMINAL_SUCCESS = "SUCCESS"
    TERMINAL_FAIL    = "FAILED"

    def _headers(self):
        api_key = getattr(settings, "SUNO_API_KEY", "")
        if not api_key:
            raise ValueError("SUNO_API_KEY is not set in settings/environment")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json",
        }

    def _build_prompt(self, request: GenerationRequest) -> str:
        """
        Combine SongForm fields into a single prompt string for Suno.
        """
        parts = [
            f"Title: {request.title}",
            f"Occasion: {request.occasion}",
            f"Mood: {request.mood}",
            f"Voice type: {request.voice_type}",
        ]
        if request.detail:
            parts.append(f"Details: {request.detail}")
        return ". ".join(parts)

    def _create_task(self, request: GenerationRequest) -> str:
        """
        POST to generate endpoint, return taskId.
        """
        payload = {
            "customMode": False,          # let Suno auto-generate lyrics
            "instrumental": False,
            "model": "V4_5ALL",
            "prompt": self._build_prompt(request),
            "style": request.genre,
            "title": request.title,
        }

        response = requests.post(
            f"{self.BASE_URL}/api/v1/generate",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        # API returns { "data": { "taskId": "..." } }
        task_id = data.get("data", {}).get("taskId")
        if not task_id:
            raise ValueError(f"No taskId in response: {data}")
        return task_id

    def _poll_for_result(self, task_id: str) -> dict:
        """
        Poll record-info until terminal status or timeout.
        Returns the first completed clip data.
        """
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            response = requests.get(
                f"{self.BASE_URL}/api/v1/generate/record-info",
                headers=self._headers(),
                params={"taskId": task_id},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            status = data.get("data", {}).get("status", "")
            clips  = data.get("data", {}).get("clips", [])

            print(f"[Suno] Attempt {attempt}/{self.MAX_ATTEMPTS} — status: {status}")

            if status == self.TERMINAL_SUCCESS and clips:
                return clips[0]   # return first generated clip

            if status == self.TERMINAL_FAIL:
                raise RuntimeError(f"Suno generation failed for taskId: {task_id}")

            time.sleep(self.POLL_INTERVAL)

        raise TimeoutError(
            f"Suno generation timed out after "
            f"{self.MAX_ATTEMPTS * self.POLL_INTERVAL}s for taskId: {task_id}"
        )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Full generation flow: create task → poll → return result.
        """
        task_id = self._create_task(request)
        print(f"[Suno] Task created: {task_id}")

        clip = self._poll_for_result(task_id)

        return GenerationResult(
            song_link  = clip.get("audio_url") or clip.get("stream_audio_url", ""),
            duration   = int(clip.get("duration", 0)),
            raw_status = self.TERMINAL_SUCCESS,
            task_id    = task_id,
        )