import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User


@method_decorator(csrf_exempt, name="dispatch")
class UserListCreateView(View):
    def get(self, request):
        users = list(User.objects.values("id", "user_name", "email", "created_at"))
        return JsonResponse(users, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create(
            user_name=data["user_name"],
            email=data["email"],
            google_oauth_id=data["google_oauth_id"],
        )
        return JsonResponse({"id": user.id, "user_name": user.user_name}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(View):
    def _get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self._get_object(pk)
        if not user:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({"id": user.id, "user_name": user.user_name, "email": user.email})

    def put(self, request, pk):
        user = self._get_object(pk)
        if not user:
            return JsonResponse({"error": "Not found"}, status=404)
        data = json.loads(request.body)
        user.user_name = data.get("user_name", user.user_name)
        user.email = data.get("email", user.email)
        user.save()
        return JsonResponse({"id": user.id, "user_name": user.user_name})

    def delete(self, request, pk):
        user = self._get_object(pk)
        if not user:
            return JsonResponse({"error": "Not found"}, status=404)
        user.delete()
        return JsonResponse({"deleted": True}, status=204)
