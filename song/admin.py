from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "created_by", "duration", "create_at")
    list_filter = ("status",)
    search_fields = ("title", "created_by")
    readonly_fields = ("create_at",)
