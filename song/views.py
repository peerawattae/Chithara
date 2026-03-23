import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Song, GenerateStatus
from library.models import Library
from song_form.models import SongForm


@method_decorator(csrf_exempt, name="dispatch")
class SongListCreateView(View):
    def get(self, request):
        # Default ordering: create_at descending (diagram note)
        songs = list(Song.objects.values(
            "id", "title", "status", "song_link",
            "created_by", "duration", "create_at", "cover_image", "library_id"
        ))
        return JsonResponse(songs, safe=False)

    def post(self, request):
        d = json.loads(request.body)
        library  = Library.objects.get(pk=d["library_id"]) if d.get("library_id") else None
        sf       = SongForm.objects.get(pk=d["song_form_id"]) if d.get("song_form_id") else None
        song = Song.objects.create(
            title=d["title"],
            status=d.get("status", GenerateStatus.IN_PROGRESS),
            song_link=d.get("song_link"),
            created_by=d["created_by"],
            duration=d.get("duration", 0),
            cover_image=d.get("cover_image"),
            library=library,
            song_form=sf,
        )
        return JsonResponse({"id": song.id, "title": song.title, "status": song.status}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class SongDetailView(View):
    def _get(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return None

    def get(self, request, pk):
        s = self._get(pk)
        if not s:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({
            "id": s.id, "title": s.title, "status": s.status,
            "song_link": s.song_link, "created_by": s.created_by,
            "duration": s.duration, "create_at": str(s.create_at),
            "cover_image": s.cover_image, "library_id": s.library_id,
            "song_form_id": s.song_form_id,
        })

    def put(self, request, pk):
        s = self._get(pk)
        if not s:
            return JsonResponse({"error": "Not found"}, status=404)
        d = json.loads(request.body)
        s.title      = d.get("title", s.title)
        s.status     = d.get("status", s.status)
        s.song_link  = d.get("song_link", s.song_link)
        s.duration   = d.get("duration", s.duration)
        s.cover_image = d.get("cover_image", s.cover_image)
        s.save()
        return JsonResponse({"id": s.id, "title": s.title, "status": s.status})

    def delete(self, request, pk):
        s = self._get(pk)
        if not s:
            return JsonResponse({"error": "Not found"}, status=404)
        s.delete()
        return JsonResponse({"deleted": True}, status=204)
