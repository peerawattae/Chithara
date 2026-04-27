import threading

from django.db import models
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import User, Creator, Library, SongForm, Song, GenerateStatus
from ..generation import get_generator, GenerationRequest
from .helpers import parse_json, not_found


@method_decorator(csrf_exempt, name="dispatch")
class SongFormListCreateView(View):
    def get(self, request):
        return JsonResponse(
            list(SongForm.objects.values(
                "id", "creator__name", "occasion", "genre",
                "voice_type", "mood", "detail", "created_at"
            )),
            safe=False,
        )

    def post(self, request):
        d = parse_json(request)

        #Get or create Creator
        try:
            creator = Creator.objects.get(pk=d["user_id"])
            creator_created = False
        except Creator.DoesNotExist:
            user = User.objects.get(pk=d["user_id"])
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO core_creator (user_ptr_id, quota) VALUES (%s, %s)",
                    [user.pk, 20]
                )
            creator = Creator.objects.get(pk=d["user_id"])
            creator_created = True

        if creator_created:
            Library.objects.create(owner=creator)

        # Enforce daily quota
        if creator.quota <= 0:
            return JsonResponse(
                {"error": "Daily generation limit reached (max 20 songs per day)"},
                status=429,
            )

        # Create SongForm
        sf = SongForm.objects.create(
            creator=creator,
            occasion=d["occasion"],
            genre=d["genre"],
            voice_type=d["voice_type"],
            mood=d["mood"],
            detail=d.get("detail", ""),
        )

        # Create Song with IN_PROGRESS status immediately
        library = Library.objects.get(owner=creator)
        song = Song.objects.create(
            title=d["title"],
            status=GenerateStatus.IN_PROGRESS,
            created_by=creator.name,
            library=library,
            song_form=sf,
        )

        # Build the generation request before spawning the thread so that
        # all data is captured from the current request context.
        gen_request = GenerationRequest(
            title=d["title"],
            occasion=d["occasion"],
            genre=d["genre"],
            voice_type=d["voice_type"],
            mood=d["mood"],
            detail=d.get("detail", ""),
        )

        # Spawn background thread
        def _run_generation(song_id, creator_id, gen_req):
            """
            Background task: call the generation strategy and persist
            the result (song_link, duration, cover_image, status) once
            Suno responds. Quota is only deducted on success.
            """
            # Import inside the thread to ensure it uses its own DB connection.
            from django.db import connection as _conn
            try:
                result = get_generator().generate(gen_req)
                # including cover_image which was previously dropped.
                Song.objects.filter(pk=song_id).update(
                    song_link   = result.song_link or None,
                    duration    = result.duration,
                    cover_image = result.cover_image or None,
                    status      = GenerateStatus.SUCCESS,
                )

                # Use F() to avoid race conditions on the quota counter.
                Creator.objects.filter(pk=creator_id).update(
                    quota=models.F("quota") - 1
                )
                print(f"[Generation] Song {song_id} succeeded — {result.song_link}")

            except Exception as exc:
                Song.objects.filter(pk=song_id).update(
                    status=GenerateStatus.FAILED,
                    error_message=str(exc),
                )
                print(f"[Generation] Song {song_id} FAILED — {exc}")

            finally:
                # Always close the thread-local DB connection so it is
                # returned to the pool and does not leak.
                _conn.close()

        threading.Thread(
            target=_run_generation,
            args=(song.id, creator.id, gen_request),
            daemon=True,  # Won't block server shutdown
        ).start()

        # Return 202 immediately
        # Client should poll GET /api/songs/<id>/ and check `status`:
        #   "in_progress" → still generating
        #   "success"     → song_link and cover_image are now populated
        #   "failed"      → generation failed
        return JsonResponse({
            "song_id": song.id,
            "title":   song.title,
            "status":  song.status,  # "in_progress"
            "message": "Generation started. Poll GET /api/songs/<id>/ for updates.",
        }, status=202)


@method_decorator(csrf_exempt, name="dispatch")
class SongFormDetailView(View):
    def _get(self, pk):
        try:
            return SongForm.objects.get(pk=pk)
        except SongForm.DoesNotExist:
            return None

    def get(self, request, pk):
        sf = self._get(pk)
        if not sf:
            return not_found()
        return JsonResponse({
            "id":         sf.id,
            "creator":    sf.creator.name,
            "occasion":   sf.occasion,
            "genre":      sf.genre,
            "voice_type": sf.voice_type,
            "mood":       sf.mood,
            "detail":     sf.detail,
        })

    def put(self, request, pk):
        sf = self._get(pk)
        if not sf:
            return not_found()
        d = parse_json(request)
        sf.occasion   = d.get("occasion",   sf.occasion)
        sf.genre      = d.get("genre",      sf.genre)
        sf.voice_type = d.get("voice_type", sf.voice_type)
        sf.mood       = d.get("mood",       sf.mood)
        sf.detail     = d.get("detail",     sf.detail)
        sf.save()
        return JsonResponse({"id": sf.id, "genre": sf.genre})

    def delete(self, request, pk):
        sf = self._get(pk)
        if not sf:
            return not_found()
        sf.delete()
        return JsonResponse({"deleted": True}, status=204)

@method_decorator(csrf_exempt, name="dispatch")
class SongFormReviewView(View):
    """
    POST /api/song-forms/review/
    Accepts form data and returns it for user confirmation
    before actual generation (FR2).
    No song or form is created — read only preview.
    """
    def post(self, request):
        d = parse_json(request)

        required = ["title", "occasion", "genre", "voice_type", "mood"]
        missing  = [f for f in required if not d.get(f)]
        if missing:
            return JsonResponse(
                {"error": f"Missing required fields: {', '.join(missing)}"},
                status=400
            )

        return JsonResponse({
            "review": {
                "title":      d["title"],
                "occasion":   d["occasion"],
                "genre":      d["genre"],
                "voice_type": d["voice_type"],
                "mood":       d["mood"],
                "detail":     d.get("detail", ""),
            },
            "message": "Please confirm to proceed with song generation",
        })