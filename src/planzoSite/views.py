from profiles.models import Profile
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, EmailAuthenticationForm
from django.shortcuts import redirect, render, redirect
# payments


from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import requests
import datetime
import base64
import json



# payments view


    
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


# Function to obtain access token
def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    auth = (settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    response = requests.get(url, auth=auth)
    access_token = response.json()['access_token']
    return access_token

# Function to initiate Lipa Na M-Pesa Online Payment (STK Push)
def lipa_na_mpesa(request):
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Generate password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')

    # STK Push request data
    data = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,  
        "PartyA": "2547XXXXXXXX",  
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": "2547XXXXXXXX",
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "TestPayment",
        "TransactionDesc": "Payment for test purposes"
    }
    
    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    response = requests.post(url, json=data, headers=headers)
    return JsonResponse(response.json())  # Returning the JSON response for debug

@csrf_exempt


def stk_push_callback(request):
    if request.method == "POST":
        payment_data = json.loads(request.body)
        
        # Check the payment result
        if payment_data.get("ResultCode") == 0:  # Success
            # Log success, update DB, notify user, etc.
            return JsonResponse({"status": "Payment Successful"})
        else:
            # Log failure
            return JsonResponse({"status": "Payment Failed", "reason": payment_data.get("ResultDesc")})

    return JsonResponse({"status": "Invalid request method"})




def pay(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")

        # Convert amount to integer
        try:
            amount = int(amount)
        except ValueError:
            return render(request, "payment_error.html", {"error": "Invalid amount. Please enter a number."})

        account_reference = "Your Reference"
        transaction_desc = "Payment for goods"
        callback_url = "https://yourdomain.com/express-payment"

        cl = MpesaClient()
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        response_data = json.loads(response.content)
        if response_data.get("ResponseCode") == "0":
            # Render intermediate page while waiting for confirmation
            return render(request, "waiting_for_confirmation.html", {
                "phone_number": phone_number,
                "amount": amount
            })
        else:
            # Failed to initiate payment
            error_message = response_data.get("errorMessage", "An error occurred during payment.")
            return render(request, "payment_error.html", {"error": error_message})

    return render(request, "pay_form.html")




def check_payment_status(request):
    payment_status = "Success"  
    if payment_status == "Success":
        return render(request, "payment_success.html")
    else:
        return render(request, "payment_error.html", {"error": "Payment not completed."})




