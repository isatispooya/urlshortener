from django.contrib import admin
from .models import Client
# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('link', 'ip_address', 'created_at')
    search_fields = ('link__original_url', 'ip_address')
