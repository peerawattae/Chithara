from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import Library, SongForm, Song, GenerateStatus
from .helpers import parse_json, not_found


@method_decorator(csrf_exempt, name="dispatch")
class SongListCreateView(View):
    def get(self, request):
        return JsonResponse(
            list(Song.objects.values(
                "id", "title", "status", "song_link",
                "created_by", "duration", "create_at", "cover_image", "library_id", "error_message"
            )),
            safe=False,
        )

    def post(self, request):
        d = parse_json(request)
        library   = Library.objects.get(pk=d["library_id"]) if d.get("library_id") else None
        song_form = SongForm.objects.get(pk=d["song_form_id"]) if d.get("song_form_id") else None
        song = Song.objects.create(
            title=d["title"],
            status=d.get("status", GenerateStatus.IN_PROGRESS),
            song_link=d.get("song_link"),
            created_by=d["created_by"],
            duration=d.get("duration", 0),
            cover_image=d.get("cover_image"),
            library=library,
            song_form=song_form,
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
            return not_found()
        return JsonResponse({
            "id": s.id, "title": s.title, "status": s.status,
            "song_link": s.song_link, "created_by": s.created_by,
            "duration": s.duration, "create_at": str(s.create_at),
            "cover_image": s.cover_image, "library_id": s.library_id,
            "error_message": s.error_message,
        })

    def put(self, request, pk):
        s = self._get(pk)
        if not s:
            return not_found()
        d = parse_json(request)
        s.title       = d.get("title",       s.title)
        s.status      = d.get("status",      s.status)
        s.song_link   = d.get("song_link",   s.song_link)
        s.duration    = d.get("duration",    s.duration)
        s.cover_image = d.get("cover_image", s.cover_image)
        s.save()
        return JsonResponse({"id": s.id, "title": s.title, "status": s.status})

    def delete(self, request, pk):
        s = self._get(pk)
        if not s:
            return not_found()
        s.delete()
        return JsonResponse({"deleted": True}, status=204)

@method_decorator(csrf_exempt, name="dispatch")
class SongDescriptionView(View):
    """
    GET /api/songs/<id>/description/
    Returns full song details combined with its SongForm input data.
    Covers FR17 (description page) and FR18 (show form details).
    """
    def get(self, request, pk):
        try:
            song = Song.objects.select_related("song_form").get(pk=pk)
        except Song.DoesNotExist:
            return not_found()

        sf = song.song_form

        return JsonResponse({
            # Song output data
            "song": {
                "id":           song.id,
                "title":        song.title,
                "status":       song.status,
                "song_link":    song.song_link,
                "duration":     song.duration,
                "cover_image":  song.cover_image,
                "created_by":   song.created_by,
                "created_at":   str(song.create_at),
                "error_message":song.error_message,
            },
            # SongForm input data (FR18)
            "form_details": {
                "occasion":   sf.occasion   if sf else None,
                "genre":      sf.genre      if sf else None,
                "voice_type": sf.voice_type if sf else None,
                "mood":       sf.mood       if sf else None,
                "detail":     sf.detail     if sf else None,
            } if sf else None,
        })

@method_decorator(csrf_exempt, name="dispatch")
class SongShareView(View):
    """
    POST /api/songs/<id>/share/
    Marks song as shared and returns a shareable URL (FR3).

    GET /api/songs/shared/<id>/
    Allows a Listener to access a shared song via link (UC6, UC7).
    """
    def post(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return not_found()

        song.is_shared = True
        song.save()

        share_url = f"/api/songs/shared/{song.id}/"
        return JsonResponse({
            "song_id":   song.id,
            "title":     song.title,
            "share_url": share_url,
            "message":   "Song shared successfully",
        })


@method_decorator(csrf_exempt, name="dispatch")
class SharedSongView(View):
    """
    GET /api/songs/shared/<id>/
    Public access to a shared song — no creator auth needed.
    """
    def get(self, request, pk):
        try:
            song = Song.objects.select_related("song_form").get(pk=pk)
        except Song.DoesNotExist:
            return not_found()

        if not song.is_shared:
            return JsonResponse(
                {"error": "This song is not shared"},
                status=403
            )

        sf = song.song_form
        return JsonResponse({
            "id":          song.id,
            "title":       song.title,
            "song_link":   song.song_link,
            "duration":    song.duration,
            "cover_image": song.cover_image,
            "created_by":  song.created_by,
            "form_details": {
                "occasion":   sf.occasion,
                "genre":      sf.genre,
                "voice_type": sf.voice_type,
                "mood":       sf.mood,
            } if sf else None,
        })

@method_decorator(csrf_exempt, name="dispatch")
class SongCoverView(View):
    """
    POST /api/songs/<id>/cover/
    Upload or update cover image URL for a song (FR5, FR6).
    Accepts JSON with cover_image_url field.
    Cover image is stored as a URL string per domain model decision (A4).
    """
    def post(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return not_found()

        d = parse_json(request)
        cover_url = d.get("cover_image_url", "").strip()

        if not cover_url:
            return JsonResponse(
                {"error": "cover_image_url is required"},
                status=400
            )

        song.cover_image = cover_url
        song.save()

        return JsonResponse({
            "song_id":     song.id,
            "title":       song.title,
            "cover_image": song.cover_image,
            "message":     "Cover image updated successfully",
        })

@method_decorator(csrf_exempt, name="dispatch")
class SongDownloadView(View):
    """
    GET /api/songs/<id>/download/
    Returns the song download URL with download metadata (FR4, FR8).
    """
    def get(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return not_found()

        if not song.song_link:
            return JsonResponse(
                {"error": "Song file is not available yet"},
                status=404
            )

        if song.status != "success":
            return JsonResponse(
                {"error": f"Song is not ready for download (status: {song.status})"},
                status=400
            )

        return JsonResponse({
            "song_id":       song.id,
            "title":         song.title,
            "download_url":  song.song_link,
            "format":        "mp3",
            "duration":      song.duration,
            "message":       "Song ready for download",
        })