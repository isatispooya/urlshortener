from django.contrib import admin
from .models import Link, Stats
# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_url', 'created_at')
    search_fields = ('original_url', 'short_url')


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ('link', 'ip_address', 'created_at')
    search_fields = ('link__original_url', 'ip_address')
