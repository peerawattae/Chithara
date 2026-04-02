from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..models import User
from .helpers import parse_json, not_found


@method_decorator(csrf_exempt, name="dispatch")
class UserListCreateView(View):
    def get(self, request):
        return JsonResponse(list(User.objects.values("id", "name", "google_oauth_id", "created_at")), safe=False)

    def post(self, request):
        d = parse_json(request)
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
        return JsonResponse({"id": u.id, "name": u.name}) if u else not_found()

    def put(self, request, pk):
        u = self._get(pk)
        if not u:
            return not_found()
        d = parse_json(request)
        u.name = d.get("name", u.name)
        u.save()
        return JsonResponse({"id": u.id, "name": u.name})

    def delete(self, request, pk):
        u = self._get(pk)
        if not u:
            return not_found()
        u.delete()
        return JsonResponse({"deleted": True}, status=204)
