from django.contrib import admin
from .models import Listener

@admin.register(Listener)
class ListenerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
