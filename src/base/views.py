from django.contrib import messages
from .forms import PetitionSignupForm
from django.shortcuts import render, redirect
 

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def petition_signup(request):
    form = PetitionSignupForm()  
    
   
    if request.method == 'POST':
        form = PetitionSignupForm(request.POST)
     
        if form.is_valid():
            form.save()  
            messages.success(request, 'Thank you for signing the petition!')  
            return redirect('home')  
    

    return render(request, 'petition_signup.html', {'form': form})