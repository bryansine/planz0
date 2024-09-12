from django.contrib import admin
from django.urls import path
from .views import editProfile, profileView

urlpatterns = [
    path('editprofile/', editProfile, name='editprofile'),
    path('profile/', profileView, name='Profile'),
]