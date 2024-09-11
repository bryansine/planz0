from django.db import models

# Create your models here.
class PetitionSignup(models.Model):
    # Define fields for a petition signup
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    message = models.TextField(blank=True, null=True)  
    signed_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        # Return the name and email of the person signing the petition
        return f'{self.name , self.email}'
    class Meta:
        # Sort the petition signups by the date they were signed up, in descending order
        ordering = ['signed_at']
        verbose_name_plural = 'Petition Signups'
        verbose_name = 'Petition Signup'
        