from django.contrib import admin
from django.urls import path, include
from core.views.pages import library_page, create_page

urlpatterns = [
    path("admin/",   admin.site.urls),
    path("api/",     include("core.urls")),
    # Frontend pages
    path("library/",                      library_page,     name="library"),
    path("create/",                       create_page,      name="create"),
]
