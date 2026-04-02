from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import Creator, Library
from .helpers import parse_json, not_found


@method_decorator(csrf_exempt, name="dispatch")
class CreatorListCreateView(View):
    def get(self, request):
        return JsonResponse(list(Creator.objects.values("id", "name", "quota", "created_at")), safe=False)

    def post(self, request):
        d = parse_json(request)
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
        return JsonResponse({"id": c.id, "name": c.name, "quota": c.quota}) if c else not_found()

    def put(self, request, pk):
        c = self._get(pk)
        if not c:
            return not_found()
        d = parse_json(request)
        c.name  = d.get("name", c.name)
        c.quota = d.get("quota", c.quota)
        c.save()
        return JsonResponse({"id": c.id, "name": c.name, "quota": c.quota})

    def delete(self, request, pk):
        c = self._get(pk)
        if not c:
            return not_found()
        c.delete()
        return JsonResponse({"deleted": True}, status=204)
