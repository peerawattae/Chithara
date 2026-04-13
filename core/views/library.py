from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import Library
from .helpers import not_found


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
            return not_found()
        songs = list(lib.songs.order_by("-create_at").values(
            "id", "title", "status", "song_link", "duration", "create_at"
        ))
        return JsonResponse({"id": lib.id, "owner": lib.owner.name, "songs": songs})

    def delete(self, request, pk):
        lib = self._get(pk)
        if not lib:
            return not_found()
        lib.delete()
        return JsonResponse({"deleted": True}, status=204)
