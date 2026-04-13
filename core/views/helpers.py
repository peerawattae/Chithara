import json
from django.http import JsonResponse


def parse_json(request):
    return json.loads(request.body)


def not_found():
    return JsonResponse({"error": "Not found"}, status=404)
