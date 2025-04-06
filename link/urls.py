from .views import LinkView
from django.urls import path

urlpatterns = [
    path('', LinkView.as_view(), name='link-list'),
    path('<str:short_url>/', LinkView.as_view(), name='link-detail'),
]
