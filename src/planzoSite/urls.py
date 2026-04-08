"""
URL configuration for planzoSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from base.views import home
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import loginView, signUpView, logoutUser, events, contact, petition_signup, about, pay, check_payment_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    
    path('login/', loginView, name='login'),
    path('signup/',signUpView, name='signup'),
    path('accounts/login/', loginView, name='login'),
    path('accounts/signup/', signUpView, name='signup'),
    path('home/', include('events.urls', namespace='events')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('daraja/', include('daraja.urls')),
    path('pay/', pay, name='pay'),
    path('check-payment-status/', check_payment_status, name='check_payment_status'),
    path('accounts/login/', loginView, name='login'),
    path('accounts/signup/', signUpView, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)