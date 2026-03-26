from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    CreatorListCreateView, CreatorDetailView,
    ListenerListCreateView, ListenerDetailView,
    LibraryListView, LibraryDetailView,
    SongFormListCreateView, SongFormDetailView,
    SongListCreateView, SongDetailView,
)

urlpatterns = [
    # Users
    path("users/",              UserListCreateView.as_view(),    name="user-list"),
    path("users/<int:pk>/",     UserDetailView.as_view(),        name="user-detail"),
    # Creators
    path("creators/",           CreatorListCreateView.as_view(), name="creator-list"),
    path("creators/<int:pk>/",  CreatorDetailView.as_view(),     name="creator-detail"),
    # Listeners
    path("listeners/",          ListenerListCreateView.as_view(),name="listener-list"),
    path("listeners/<int:pk>/", ListenerDetailView.as_view(),    name="listener-detail"),
    # Libraries
    path("libraries/",          LibraryListView.as_view(),       name="library-list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(),     name="library-detail"),
    # Song forms
    path("song-forms/",         SongFormListCreateView.as_view(),name="songform-list"),
    path("song-forms/<int:pk>/",SongFormDetailView.as_view(),    name="songform-detail"),
    # Songs
    path("songs/",              SongListCreateView.as_view(),    name="song-list"),
    path("songs/<int:pk>/",     SongDetailView.as_view(),        name="song-detail"),
]
