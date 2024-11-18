from django.urls import path
from . import views

app_name = 'daraja' 

urlpatterns = [
    path('lipa-na-mpesa/', views.lipa_na_mpesa, name='lipa_na_mpesa'),
    path('stk-push-callback/', views.stk_push_callback, name='stk_push_callback'),    
             ]