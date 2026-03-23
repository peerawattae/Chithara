from django.contrib import admin
from .models import Creator

@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quota", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
