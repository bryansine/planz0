from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
import base64
from django.conf import settings

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
        "Amount": 1,  # Change to the required amount
        "PartyA": "2547XXXXXXXX",  # Replace with the payer's phone number
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
    if request.method == 'POST':
        payment_data = request.body.decode('utf-8')
        # Parse the JSON data received and log it
        print(payment_data)
        # Process payment_data as required, for example, saving transaction data
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})  # Required for Daraja
    return HttpResponse("Invalid request method.", status=400)

# from django.http import JsonResponse

# def check_payment_status(request):
#     payment_status = "Pending"
#     if payment_status == "Success":
#         return JsonResponse({"status": "Success"})
#     elif payment_status == "Failed":
#         return JsonResponse({"status": "Failed"})
#     else:
#         return JsonResponse({"status": "Pending"})