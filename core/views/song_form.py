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
 
        # Get or create Creator directly by user id
        try:
            creator = Creator.objects.get(pk=d["user_id"])
            creator_created = False
        except Creator.DoesNotExist:
            # Grab the existing user row data first
            user = User.objects.get(pk=d["user_id"])
            # Use raw update to add the creator row without touching core_user
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

        #Enforce daily quota
        if creator.quota <= 0:
            return JsonResponse(
                {"error": "Daily generation limit reached (max 20 songs per day)"},
                status=429,
            )

        #Create SongForm
        sf = SongForm.objects.create(
            creator=creator,
            occasion=d["occasion"],
            genre=d["genre"],
            voice_type=d["voice_type"],
            mood=d["mood"],
            detail=d.get("detail", ""),
        )

        #Create Song with IN_PROGRESS status
        library = Library.objects.get(owner=creator)
        song = Song.objects.create(
            title=d["title"],
            status=GenerateStatus.IN_PROGRESS,
            created_by=creator.name,
            library=library,
            song_form=sf,
        )

        #Call the active generation strategy
        try:
            gen_request = GenerationRequest(
                title=d["title"],
                occasion=d["occasion"],
                genre=d["genre"],
                voice_type=d["voice_type"],
                mood=d["mood"],
                detail=d.get("detail", ""),
            )
            result = get_generator().generate(gen_request)

            #Generation succeeded — update Song
            song.song_link = result.song_link
            song.duration  = result.duration
            song.status    = GenerateStatus.SUCCESS
            song.save()

            creator.quota -= 1
            creator.save()

            return JsonResponse({
                "song_id":   song.id,
                "title":     song.title,
                "status":    song.status,
                "song_link": song.song_link,
                "duration":  song.duration,
                "task_id":   result.task_id,
            }, status=201)

        except RuntimeError as e:
            song.status = GenerateStatus.FAILED
            song.save()

            # Detect credit error specifically
            error_msg = str(e)
            status_code = 402 if "credits insufficient" in error_msg else 500
            return JsonResponse({
                "song_id": song.id,
                "title":   song.title,
                "status":  song.status,
                "error":   error_msg,
            }, status=status_code)

        except Exception as e:
            song.status = GenerateStatus.FAILED
            song.save()
            return JsonResponse({
                "song_id": song.id,
                "title":   song.title,
                "status":  song.status,
                "error":   str(e),
            }, status=500)
        

        except Exception as e:
            #Generation failed — mark Song as FAILED
            # Quota is NOT deducted on failure (BR2)
            song.status = GenerateStatus.FAILED
            song.save()

            return JsonResponse({
                "song_id": song.id,
                "title":   song.title,
                "status":  song.status,
                "error":   str(e),
            }, status=500)


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