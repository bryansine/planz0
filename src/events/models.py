from django.db import models
from profiles.models import Profile

# create models here
class Event(models.Model):
    organizer   = models.ForeignKey(Profile, related_name='organizer', on_delete=models.CASCADE)
    attendees   = models.ManyToManyField(Profile, blank=True, default=None, related_name='attendees')
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    poster      = models.ImageField(upload_to='EventPoster/', blank=True)
    venue       = models.CharField(max_length=100)
    size        = models.PositiveIntegerField()
    price       = models.PositiveIntegerField()  
    date        = models.DateTimeField()
    ksh         = models.PositiveIntegerField(blank=True) 
    updated     = models.TimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}   -->  id : {self.id}" 
    
    class Meta:
        ordering = ('-created',)
        