
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('link.urls')),
    path('stats/', include('stats.urls')),
]
