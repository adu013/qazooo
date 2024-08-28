from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['original_url', 'created_by', 'created_at', 'updated_at',]
    list_filter = ['created_by',]
