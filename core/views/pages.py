from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import User, Creator, Library


def get_domain_user(request):
    """
    Returns our domain User from the session.
    Returns None if not logged in or no domain user yet.
    """
    uid = request.session.get("domain_user_id")
    if not uid:
        return None
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        return None


def login_page(request):
    # Already logged in → go to library
    if request.user.is_authenticated:
        return redirect("/library/")
    return render(request, "core/login.html")


@login_required
def library_page(request):
    domain_user = get_domain_user(request)
    return render(request, "core/library.html", {
        "domain_user_id":   domain_user.pk   if domain_user else None,
        "domain_user_name": domain_user.name if domain_user else request.user.get_full_name(),
    })


@login_required
def create_page(request):
    domain_user = get_domain_user(request)
    return render(request, "core/create.html", {
        "domain_user_id": domain_user.pk if domain_user else None,
    })


@login_required
def song_page(request, pk):
    domain_user = get_domain_user(request)
    return render(request, "core/song.html", {
        "song_id":        pk,
        "domain_user_id": domain_user.pk if domain_user else None,
    })


@login_required
def description_page(request, pk):
    domain_user = get_domain_user(request)
    return render(request, "core/description.html", {
        "song_id":        pk,
        "domain_user_id": domain_user.pk if domain_user else None,
    })


def shared_song_page(request, pk):
    """
    Public page — no login required.
    Listener opens a shared song link.
    """
    return render(request, "core/shared.html", {"song_id": pk})