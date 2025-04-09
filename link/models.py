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
    


