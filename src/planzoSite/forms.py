from django import forms
from profiles.models import PROFILE_TYPE_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, required=True, help_text='Required. Enter a valid email address.')
    role = forms.ChoiceField(
        choices =PROFILE_TYPE_CHOICES,
        required=True,
        widget  =forms.Select(attrs={'class': 'userInputRole'}),
        )
    class Meta:
        model  = User
        fields = ('username', 'role', 'email', 'password1', 'password2')


# class EmailAuthenticationForm(forms.Form):
#     username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'}))


class EmailAuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=254, 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True
    )