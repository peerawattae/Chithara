from django.urls import path
from .views import SongFormListCreateView, SongFormDetailView

urlpatterns = [
    path("", SongFormListCreateView.as_view(), name="songform-list-create"),
    path("<int:pk>/", SongFormDetailView.as_view(), name="songform-detail"),
]
