from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/",         admin.site.urls),
    path("api/users/",     include("user.urls")),
    path("api/creators/",  include("creator.urls")),
    path("api/listeners/", include("listener.urls")),
    path("api/libraries/", include("library.urls")),
    path("api/song-forms/",include("song_form.urls")),
    path("api/songs/",     include("song.urls")),
]
