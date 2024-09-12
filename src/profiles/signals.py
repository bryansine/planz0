from .models import Profile
from django.dispatch import receiver
from django.contrib.auth.models import User
# from django.db.models.signals import post_save

# @receiver(post_save, sender=User)
# def createUserProfile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def saveUserProfile(sender, instance, **kwargs):
#     instance.profile.save()