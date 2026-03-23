from django.contrib import admin
from .models import Library

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "created_at")
    search_fields = ("owner__name",)
    readonly_fields = ("created_at",)
