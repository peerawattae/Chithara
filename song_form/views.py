import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import SongForm, GenreChoices


@method_decorator(csrf_exempt, name="dispatch")
class SongFormListCreateView(View):
    def get(self, request):
        forms = list(SongForm.objects.values("id", "occasion", "genre", "voice_type", "mood", "detail"))
        return JsonResponse(forms, safe=False)

    def post(self, request):
        d = json.loads(request.body)
        sf = SongForm.objects.create(
            occasion=d["occasion"],
            genre=d["genre"],
            voice_type=d["voice_type"],
            mood=d["mood"],
            detail=d.get("detail", ""),
        )
        return JsonResponse({"id": sf.id, "genre": sf.genre}, status=201)


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
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({"id": sf.id, "occasion": sf.occasion, "genre": sf.genre,
                             "voice_type": sf.voice_type, "mood": sf.mood, "detail": sf.detail})

    def put(self, request, pk):
        sf = self._get(pk)
        if not sf:
            return JsonResponse({"error": "Not found"}, status=404)
        d = json.loads(request.body)
        sf.occasion   = d.get("occasion", sf.occasion)
        sf.genre      = d.get("genre", sf.genre)
        sf.voice_type = d.get("voice_type", sf.voice_type)
        sf.mood       = d.get("mood", sf.mood)
        sf.detail     = d.get("detail", sf.detail)
        sf.save()
        return JsonResponse({"id": sf.id, "genre": sf.genre})

    def delete(self, request, pk):
        sf = self._get(pk)
        if not sf:
            return JsonResponse({"error": "Not found"}, status=404)
        sf.delete()
        return JsonResponse({"deleted": True}, status=204)
