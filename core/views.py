import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import (
    User, Creator, Listener,
    Library, SongForm, Song,
    GenerateStatus,
)


def _json(request):
    return json.loads(request.body)


def _not_found():
    return JsonResponse({"error": "Not found"}, status=404)


# User
@method_decorator(csrf_exempt, name="dispatch")
class UserListCreateView(View):
    def get(self, request):
        return JsonResponse(list(User.objects.values("id", "name", "google_oauth_id", "created_at")), safe=False)

    def post(self, request):
        d = _json(request)
        u = User.objects.create(
            name=d["name"],
            google_oauth_id=d.get("google_oauth_id"),
        )
        return JsonResponse({"id": u.id, "name": u.name}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(View):
    def _get(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        u = self._get(pk)
        return JsonResponse({"id": u.id, "name": u.name}) if u else _not_found()

    def put(self, request, pk):
        u = self._get(pk)
        if not u:
            return _not_found()
        d = _json(request)
        u.name = d.get("name", u.name)
        u.save()
        return JsonResponse({"id": u.id, "name": u.name})

    def delete(self, request, pk):
        u = self._get(pk)
        if not u:
            return _not_found()
        u.delete()
        return JsonResponse({"deleted": True}, status=204)


# Creator
@method_decorator(csrf_exempt, name="dispatch")
class CreatorListCreateView(View):
    def get(self, request):
        return JsonResponse(list(Creator.objects.values("id", "name", "quota", "created_at")), safe=False)

    def post(self, request):
        d = _json(request)
        c = Creator.objects.create(
            name=d["name"],
            google_oauth_id=d.get("google_oauth_id"),
            quota=d.get("quota", 20),
        )
        Library.objects.create(owner=c)   # Library created alongside Creator
        return JsonResponse({"id": c.id, "name": c.name, "quota": c.quota}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CreatorDetailView(View):
    def _get(self, pk):
        try:
            return Creator.objects.get(pk=pk)
        except Creator.DoesNotExist:
            return None

    def get(self, request, pk):
        c = self._get(pk)
        return JsonResponse({"id": c.id, "name": c.name, "quota": c.quota}) if c else _not_found()

    def put(self, request, pk):
        c = self._get(pk)
        if not c:
            return _not_found()
        d = _json(request)
        c.name  = d.get("name", c.name)
        c.quota = d.get("quota", c.quota)
        c.save()
        return JsonResponse({"id": c.id, "name": c.name, "quota": c.quota})

    def delete(self, request, pk):
        c = self._get(pk)
        if not c:
            return _not_found()
        c.delete()
        return JsonResponse({"deleted": True}, status=204)


# Listener
@method_decorator(csrf_exempt, name="dispatch")
class ListenerListCreateView(View):
    def get(self, request):
        return JsonResponse(list(Listener.objects.values("id", "name", "created_at")), safe=False)

    def post(self, request):
        d = _json(request)
        l = Listener.objects.create(
            name=d["name"],
            google_oauth_id=d.get("google_oauth_id"),
        )
        return JsonResponse({"id": l.id, "name": l.name}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class ListenerDetailView(View):
    def _get(self, pk):
        try:
            return Listener.objects.get(pk=pk)
        except Listener.DoesNotExist:
            return None

    def get(self, request, pk):
        l = self._get(pk)
        return JsonResponse({"id": l.id, "name": l.name}) if l else _not_found()

    def put(self, request, pk):
        l = self._get(pk)
        if not l:
            return _not_found()
        d = _json(request)
        l.name = d.get("name", l.name)
        l.save()
        return JsonResponse({"id": l.id, "name": l.name})

    def delete(self, request, pk):
        l = self._get(pk)
        if not l:
            return _not_found()
        l.delete()
        return JsonResponse({"deleted": True}, status=204)


# Library
@method_decorator(csrf_exempt, name="dispatch")
class LibraryListView(View):
    def get(self, request):
        return JsonResponse(list(Library.objects.values("id", "owner__name", "created_at")), safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class LibraryDetailView(View):
    def _get(self, pk):
        try:
            return Library.objects.get(pk=pk)
        except Library.DoesNotExist:
            return None

    def get(self, request, pk):
        lib = self._get(pk)
        if not lib:
            return _not_found()
        songs = list(lib.songs.order_by("-create_at").values(
            "id", "title", "status", "song_link", "duration", "create_at"
        ))
        return JsonResponse({"id": lib.id, "owner": lib.owner.name, "songs": songs})

    def delete(self, request, pk):
        lib = self._get(pk)
        if not lib:
            return _not_found()
        lib.delete()
        return JsonResponse({"deleted": True}, status=204)


# SongForm
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
        d = _json(request)

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
            return _not_found()
        return JsonResponse({
            "id": sf.id, "creator": sf.creator.name,
            "occasion": sf.occasion, "genre": sf.genre,
            "voice_type": sf.voice_type, "mood": sf.mood, "detail": sf.detail,
        })

    def put(self, request, pk):
        sf = self._get(pk)
        if not sf:
            return _not_found()
        d = _json(request)
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
            return _not_found()
        sf.delete()
        return JsonResponse({"deleted": True}, status=204)


# Song
@method_decorator(csrf_exempt, name="dispatch")
class SongListCreateView(View):
    def get(self, request):
        return JsonResponse(
            list(Song.objects.values(
                "id", "title", "status", "song_link",
                "created_by", "duration", "create_at", "cover_image", "library_id",
            )),
            safe=False,
        )

    def post(self, request):
        d = _json(request)
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
            return _not_found()
        return JsonResponse({
            "id": s.id, "title": s.title, "status": s.status,
            "song_link": s.song_link, "created_by": s.created_by,
            "duration": s.duration, "create_at": str(s.create_at),
            "cover_image": s.cover_image, "library_id": s.library_id,
        })

    def put(self, request, pk):
        s = self._get(pk)
        if not s:
            return _not_found()
        d = _json(request)
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
            return _not_found()
        s.delete()
        return JsonResponse({"deleted": True}, status=204)
