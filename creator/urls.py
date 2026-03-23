from django.urls import path
from .views import CreatorListCreateView, CreatorDetailView

urlpatterns = [
    path("", CreatorListCreateView.as_view(), name="creator-list-create"),
    path("<int:pk>/", CreatorDetailView.as_view(), name="creator-detail"),
]
