from django.urls import path
from .views import ListenerListCreateView, ListenerDetailView

urlpatterns = [
    path("", ListenerListCreateView.as_view(), name="listener-list-create"),
    path("<int:pk>/", ListenerDetailView.as_view(), name="listener-detail"),
]
