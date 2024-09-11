from django import forms
from .models import PetitionSignup

class PetitionSignupForm(forms.ModelForm):
    class Meta:
        model = PetitionSignup
        fields = ['name', 'email', 'message']