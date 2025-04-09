from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    link_short_url = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = '__all__'

    def get_link_short_url(self, obj):
        return obj.link.short_url

