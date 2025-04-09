from django.contrib import admin
from .models import Link
# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_url', 'created_at')
    search_fields = ('original_url', 'short_url')


