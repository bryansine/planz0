from .models import Profile # profile import

def profile_authenticated(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        return {'profile_obj': profile_obj, }
    return {}
