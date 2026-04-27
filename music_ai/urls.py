from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views.pages import (
    login_page, library_page, create_page,
    song_page, description_page, shared_song_page,
)

urlpatterns = [
    path("admin/",   admin.site.urls),
    path("api/",     include("core.urls")),
    # Frontend pages
    path("library/",                      library_page,     name="library"),
    path("create/",                       create_page,      name="create"),
    path("songs/<int:pk>/",               song_page,        name="song-page"),
    path("songs/<int:pk>/description/",   description_page, name="description-page"),

    # OAuth
    path("auth/",    include("social_django.urls", namespace="social")),
 
    # Auth pages
    path("",         login_page,    name="home"),
    path("login/",   login_page,    name="login"),
    path("logout/",  auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),
]
