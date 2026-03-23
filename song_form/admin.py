from django.contrib import admin
from .models import SongForm

@admin.register(SongForm)
class SongFormAdmin(admin.ModelAdmin):
    list_display = ("id", "occasion", "genre", "voice_type", "mood")
    list_filter = ("genre",)
    search_fields = ("occasion", "mood")
