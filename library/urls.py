from django.urls import path
from .views import LibraryListCreateView, LibraryDetailView

urlpatterns = [
    path("", LibraryListCreateView.as_view(), name="library-list-create"),
    path("<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
]
