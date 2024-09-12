from profiles.models import Profile
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, EmailAuthenticationForm
from django.shortcuts import redirect, render, redirect


# def loginView(request):
#     if request.method == 'POST':
#         form = EmailAuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home:home')
#     else:
#         form = EmailAuthenticationForm()
#     return render(request, 'registration/login.html', { 'form': form })
    
    
def loginView(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)  # Pass only request.POST
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home:home')
            else:
                # Add an error message to indicate invalid login
                form.add_error(None, "Invalid username or password")
    else:
        form = EmailAuthenticationForm()
        
    return render(request, 'registration/login.html', {'form': form})
    
    
    
    

def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = Profile.objects.create(user=user)
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            profile.role = role
            profile.email = email
            profile.save()

            login(request, user)

            return redirect('home:home')
    else:
        form = SignUpForm()

    return render(request, 'authentication/signup.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('home')

def events(request):
    return render(request, 'events.html')

def contact(request):
    return render(request, 'contact.html')

def petition_signup(request):
    return render(request, 'petition_signup.html')

def about(request):
    return render(request, 'about.html')