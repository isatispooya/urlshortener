from django.db import models
import random
import string

# Create your models here.

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))

class Link(models.Model):
    original_url = models.URLField(unique=True)
    short_url = models.CharField(max_length=7, unique=True, default=generate_short_url)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_url
    

class Stats(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    is_routable = models.BooleanField(default=False)  # نشان می‌دهد آیا IP عمومی است یا خصوصی
    user_agent = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    browser = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
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


