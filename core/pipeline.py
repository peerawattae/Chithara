"""
core/pipeline.py

Custom social-auth pipeline step.
Runs after Django's built-in user creation step.
Creates our domain User + Creator rows linked to the Django auth user.
"""
from django.db import connection

from core.models import User, Creator, Library


def create_domain_user(backend, user, response, *args, **kwargs):
    """
    After Google OAuth creates a Django auth.User, this step:
    1. Creates (or finds) our domain User linked to auth.User
    2. Promotes them to Creator
    3. Creates their Library if it doesn't exist yet
    """
    name  = response.get("name") or user.get_full_name() or user.username
    email = response.get("email") or user.email
    google_id = response.get("sub") or str(user.id)

    # Find or create our domain User by google_oauth_id
    domain_user, _ = User.objects.get_or_create(
        google_oauth_id=google_id,
        defaults={"name": name},
    )

    # Update name if it changed
    if domain_user.name != name:
        domain_user.name = name
        domain_user.save(update_fields=["name"])

    # Promote to Creator if not already
    if not Creator.objects.filter(pk=domain_user.pk).exists():
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO core_creator (user_ptr_id, quota) VALUES (%s, %s)",
                [domain_user.pk, 20]
            )

    creator = Creator.objects.get(pk=domain_user.pk)

    # Create Library if not already
    if not Library.objects.filter(owner=creator).exists():
        Library.objects.create(owner=creator)

    # Store domain_user id in session for use in views
    kwargs["request"].session["domain_user_id"] = domain_user.pk