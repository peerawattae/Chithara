import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Library
from creator.models import Creator


@method_decorator(csrf_exempt, name="dispatch")
class LibraryListCreateView(View):
    def get(self, request):
        libs = list(Library.objects.values("id", "owner__name", "created_at"))
        return JsonResponse(libs, safe=False)

    def post(self, request):
        d = json.loads(request.body)
        owner = Creator.objects.get(pk=d["creator_id"])
        lib = Library.objects.create(owner=owner)
        return JsonResponse({"id": lib.id, "owner": owner.name}, status=201)


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
            return JsonResponse({"error": "Not found"}, status=404)
        # Songs ordered by create_at descending (diagram note)
        songs = list(lib.songs.order_by("-create_at").values("id", "title", "status", "create_at"))
        return JsonResponse({"id": lib.id, "owner": lib.owner.name, "songs": songs})

    def delete(self, request, pk):
        lib = self._get(pk)
        if not lib:
            return JsonResponse({"error": "Not found"}, status=404)
        lib.delete()
        return JsonResponse({"deleted": True}, status=204)
