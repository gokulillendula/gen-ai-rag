from django.urls import path,include
from .views import chat, home
urlpatterns = [
    path("home/", home),

    path('chat/', chat, name='chat'),
]