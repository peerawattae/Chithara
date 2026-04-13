from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import Listener
from .helpers import parse_json, not_found


@method_decorator(csrf_exempt, name="dispatch")
class ListenerListCreateView(View):
    def get(self, request):
        return JsonResponse(list(Listener.objects.values("id", "name", "created_at")), safe=False)

    def post(self, request):
        d = parse_json(request)
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
        return JsonResponse({"id": l.id, "name": l.name}) if l else not_found()

    def put(self, request, pk):
        l = self._get(pk)
        if not l:
            return not_found()
        d = parse_json(request)
        l.name = d.get("name", l.name)
        l.save()
        return JsonResponse({"id": l.id, "name": l.name})

    def delete(self, request, pk):
        l = self._get(pk)
        if not l:
            return not_found()
        l.delete()
        return JsonResponse({"deleted": True}, status=204)
