from django.contrib import admin
from .models import User, Creator, Listener, Library, SongForm, Song


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display  = ("id", "name", "quota", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Listener)
class ListenerAdmin(admin.ModelAdmin):
    list_display  = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display  = ("id", "owner", "created_at")
    search_fields = ("owner__name",)
    readonly_fields = ("created_at",)


@admin.register(SongForm)
class SongFormAdmin(admin.ModelAdmin):
    list_display  = ("id", "creator", "occasion", "genre", "created_at")
    list_filter   = ("genre",)
    search_fields = ("occasion", "creator__name")
    readonly_fields = ("created_at",)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display  = ("id", "title", "status", "created_by", "duration", "create_at")
    list_filter   = ("status",)
    search_fields = ("title", "created_by")
    readonly_fields = ("create_at",)
