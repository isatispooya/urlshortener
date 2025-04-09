from django.db import models
from link.models import Link
# Create your models here.
class Client(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    is_routable = models.BooleanField(default=False)  # نشان می‌دهد آیا IP عمومی است یا خصوصی
    user_agent = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    browser = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    utm_source = models.CharField(max_length=255, null=True, blank=True)
    utm_medium = models.CharField(max_length=255, null=True, blank=True)
    utm_campaign = models.CharField(max_length=255, null=True, blank=True)
    utm_content = models.CharField(max_length=255, null=True, blank=True)
    utm_term = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'آمار بازدید'
        verbose_name_plural = 'آمار بازدیدها'

    def __str__(self):
        return f"{self.link.short_url} - {self.ip_address}"

