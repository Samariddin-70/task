# project/urls.py
from django.urls import path, include

urlpatterns = [
    path('cards/', include('cards.card.urls')),
]

