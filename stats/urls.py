from django.urls import path
from .views import ClientListView


urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list')
    
]

