import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Creator


@method_decorator(csrf_exempt, name="dispatch")
class CreatorListCreateView(View):
    def get(self, request):
        data = list(Creator.objects.values("id", "name", "email", "quota", "created_at"))
        return JsonResponse(data, safe=False)

    def post(self, request):
        d = json.loads(request.body)
        creator = Creator.objects.create(
            name=d["name"],
            email=d["email"],
            google_oauth_id=d["google_oauth_id"],
            quota=d.get("quota", 20),
        )
        return JsonResponse({"id": creator.id, "name": creator.name}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CreatorDetailView(View):
    def _get(self, pk):
        try:
            return Creator.objects.get(pk=pk)
        except Creator.DoesNotExist:
            return None

    def get(self, request, pk):
        c = self._get(pk)
        if not c:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({"id": c.id, "name": c.name, "email": c.email, "quota": c.quota})

    def put(self, request, pk):
        c = self._get(pk)
        if not c:
            return JsonResponse({"error": "Not found"}, status=404)
        d = json.loads(request.body)
        c.name  = d.get("name", c.name)
        c.quota = d.get("quota", c.quota)
        c.save()
        return JsonResponse({"id": c.id, "name": c.name, "quota": c.quota})

    def delete(self, request, pk):
        c = self._get(pk)
        if not c:
            return JsonResponse({"error": "Not found"}, status=404)
        c.delete()
        return JsonResponse({"deleted": True}, status=204)
