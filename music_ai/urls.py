from django.contrib import admin
from django.urls import path, include
from core.views import library_page

urlpatterns = [
    path("admin/",   admin.site.urls),
    path("api/",     include("core.urls")),
    # Frontend pages
    path("library/",                      library_page,     name="library"),
]
