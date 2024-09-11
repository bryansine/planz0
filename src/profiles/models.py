from django.db import models
from django.contrib.auth.models import User

# Create your models here.
PROFILE_TYPE_CHOICES = (
    ('organizer', 'Organizer'),
    ('attendee', 'Attendee'),
)

# create class models here
class Profile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    role           = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES) 
    profilePicture = models.ImageField(default='userPlaceHolder.png', upload_to='ProfilePictures')
    firstName      = models.CharField(max_length=35, blank=True)
    lastName       = models.CharField(max_length=35, blank=True)
    email          = models.EmailField(max_length=90, blank=True)
    updated        = models.TimeField(auto_now=True)
    created        = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
