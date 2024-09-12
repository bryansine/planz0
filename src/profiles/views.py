from .models import Profile
from .forms import EditForm
from events.models import Event
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required

# @login_required
def profileView(request): # profile view
    profile       = Profile.objects.get(user=request.user) # Get the profile instance associated with the current user
    profileEvents = Event.objects.filter(organizer=profile) # Get events where the organizer is the current profile
    template      = loader.get_template('profiles/profile.html')
    context  = {
        'profile'       : profile,
        'profileEvents' : profileEvents,
    }
    return HttpResponse(template.render(context, request))


# @login_required
def editProfile(request):  # editing profile
    profile  = Profile.objects.get(user=request.user) # Get the profile instance 
    form     = EditForm(request.POST or None, request.FILES or None, instance=profile) # Create an instance of the edit form,
    if request.method == 'POST':     # Check if the form is being submitted via POST method
        if form.is_valid(): # Check if the form data is valid
            form.save()
            return redirect('profiles:profile')
    template = loader.get_template('profiles/editProfile.html')
    context = {
        'profile':profile,
        'form'   :form,
    }
    return HttpResponse(template.render(context, request))
