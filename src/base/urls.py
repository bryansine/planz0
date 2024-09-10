from .views import home, about, petition_signup
from django.urls import path

urlpatterns = [
   
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('petition_signup/', petition_signup, name='petition_signup'),
]
