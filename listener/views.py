import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Listener


@method_decorator(csrf_exempt, name="dispatch")
class ListenerListCreateView(View):
    def get(self, request):
        data = list(Listener.objects.values("id", "name", "email", "created_at"))
        return JsonResponse(data, safe=False)

    def post(self, request):
        d = json.loads(request.body)
        listener = Listener.objects.create(
            name=d["name"],
            email=d["email"],
            google_oauth_id=d["google_oauth_id"],
        )
        return JsonResponse({"id": listener.id, "name": listener.name}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class ListenerDetailView(View):
    def _get(self, pk):
        try:
            return Listener.objects.get(pk=pk)
        except Listener.DoesNotExist:
            return None

    def get(self, request, pk):
        l = self._get(pk)
        if not l:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({"id": l.id, "name": l.name, "email": l.email})

    def put(self, request, pk):
        l = self._get(pk)
        if not l:
            return JsonResponse({"error": "Not found"}, status=404)
        d = json.loads(request.body)
        l.name = d.get("name", l.name)
        l.save()
        return JsonResponse({"id": l.id, "name": l.name})

    def delete(self, request, pk):
        l = self._get(pk)
        if not l:
            return JsonResponse({"error": "Not found"}, status=404)
        l.delete()
        return JsonResponse({"deleted": True}, status=204)
