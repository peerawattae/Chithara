from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import User, Creator, Library, SongForm
from .helpers import parse_json, not_found


@method_decorator(csrf_exempt, name="dispatch")
class SongFormListCreateView(View):
    def get(self, request):
        return JsonResponse(
            list(SongForm.objects.values("id", "creator__name", "occasion", "genre", "voice_type", "mood", "detail", "created_at")),
            safe=False,
        )

    def post(self, request):
        """
        On POST:
        1. get_or_create Creator for the given user
        2. get_or_create Library for that Creator
        3. Create SongForm
        The actual AI generation call would happen here too (not implemented yet).
        """
        d = parse_json(request)

        # User becomes Creator automatically on first submission
        user = User.objects.get(pk=d["user_id"])
        creator, creator_created = Creator.objects.get_or_create(
            user_ptr=user,
            defaults={"quota": 20},
        )
        if creator_created:
            Library.objects.create(owner=creator)

        sf = SongForm.objects.create(
            creator=creator,
            occasion=d["occasion"],
            genre=d["genre"],
            voice_type=d["voice_type"],
            mood=d["mood"],
            detail=d.get("detail", ""),
        )
        return JsonResponse({"id": sf.id, "genre": sf.genre, "creator": creator.name}, status=201)


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
            "id": sf.id, "creator": sf.creator.name,
            "occasion": sf.occasion, "genre": sf.genre,
            "voice_type": sf.voice_type, "mood": sf.mood, "detail": sf.detail,
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
