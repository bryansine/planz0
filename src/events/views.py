import hashlib
from .models import Event
from django.template import loader
from profiles.models import Profile
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import EventCreationForm, EventEditForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .utils import generateUUID
from django.conf import settings
from django.template.loader import render_to_string

# qr code imports
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage


@login_required
def homeView(request):
    profile = Profile.objects.get(user=request.user) # Get the user's profile
    form    = EventCreationForm(request.POST or None, request.FILES or None) # Create an instance of EventCreationForm with POST data if available, or None
    events  = Event.objects.all()  # Retrieve all events from the Event model
    if request.method == 'POST': 
        if form.is_valid():
            event = form.save(commit=False) # save form data to create a new event
            event.organizer = profile   # Assigns the organizer of the event to the user's profile
            event.ksh = float(event.price) * 130.00   
            event.save()
            event.attendees.add(profile) # Add the user's profile as an attendee of the event

            # Set a flag in the session to indicate a successful event creation
            request.session['eventCreated'] = True

    template = loader.get_template('events/home.html') # load template
    context  = {
        "profile": profile,
        'form'   : form,
        'events' : events,
    }
    return HttpResponse(template.render(context, request))



@login_required
def eventDetailView(request, id):
    profile = Profile.objects.get(user=request.user) # get the profile from the request object
    event = Event.objects.get(pk=id) #

    profileEmail = profile.email # get the email address of the profile
    profileName = profile # get the name of the profile
    senderEmail = settings.DEFAULT_FROM_EMAIL # get the email address of the sender
    eventName = event.title # get the name of the event
    eventLocation = event.venue 
    uuid = generateUUID(profileEmail)
    profileSubject = f'Your tickets for : {eventName} {eventLocation}'

    if request.method == 'POST': 
        if profile not in event.attendees.all():   # Check if the profile is not already in the list of event attendees
            sendUUID(profileSubject, profileName, senderEmail, profileEmail, uuid, event) # Send an email with a unique UUID to the profile
            event.attendees.add(profile) # Add the profile to the list of event attendees
            request.session['eventBooked'] = True  # Set a session variable indicating that the event has been booked

    template = loader.get_template('events/eventDetail.html')
    context = {
        'event': event,
        'profile': profile,
        'uuid': uuid,  
    }
    return HttpResponse(template.render(context, request))

def sendUUID(subject, name, from_email, to_email, uuid, event):
    message = render_to_string('email_template.html', {
        'name': name,
        'uuid': uuid,
        'event': event,
    })
    send_mail(subject, message, from_email, [to_email]) # Send the email using Django's send_mail function

def generateUUID(email):
    hashObject = hashlib.sha1(email.encode())  # Create a hash object and encode the email
    hexDigit = hashObject.hexdigest() # Convert the hash to a hexadecimal string
    uuid = '-'.join([hexDigit[:3], hexDigit[3:6], hexDigit[6:9]])
    return uuid

# def sendUUID(subject, recipient_name, sender_email, recipient_email, uuid, event):
#     message = f"""
#     Dear {recipient_name},

#     We hope you're as excited as we are because you’re about to experience an unforgettable event! 🎟️✨

#     Here are your exclusive ticket details:

#     **Event Name:** {event.title}
#     **Secret Code:** {uuid}
#     **Date:** {event.date}

#     Make sure to keep this secret code safe. It's your golden ticket to an amazing time!

#     We're thrilled to have you join us and can't wait to see you there!

#     Best regards,
#     planzO) Events Team
#     """
#     send_mail(subject, message, 'planzO) Events <planzoevents@gmail.com>', [recipient_email], fail_silently=False)



def sendUUID(subject, recipient_name, sender_email, recipient_email, uuid, event, from_name):
    # Generate QR code data
    # qr_data = f"Event: {event.title}\nDate: {event.date}\nLocation: {event.venue}\nSecret Code: {uuid}"
    qr_data = f"https://triply.co/675365ab2e880d3400993e10"
    
    # Create QR code object
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    qr_code_file = ContentFile(buffer.getvalue(), name=f"{event.title}_ticket.png")
    
    #     # Path to the Triply logo image
    # logo_path = "planz0/src/static/images/tripply1.png"
    # with open(logo_path, "rb") as logo_file:
    #     logo_data = logo_file.read()

    # Generate your email content
    message = f"""
    <html>
    <body>
        
        <h3>Dear {recipient_name},</h3>

        <p>Thank you for choosing <strong>Triply.co</strong> to buy your ticket for the upcoming event!</p>
        <p>To view your ticket details, simply click the link below:</p>
        <p><a href="https://triply.co/675365ab2e880d3400993e10" target="_blank">https://triply.co/675365ab2e880d3400993e10</a></p>

        <p>We are committed to making your trip with Triply.co a memorable one. If you have any special requests or requirements, 
        please let us know, and we will do our best to accommodate them.</p>

        <p>Thank you again for choosing Triply.co. We look forward to creating amazing memories with you!</p>

        <p>For any inquiries or assi        # Path to the Triply logo image
    logo_path = "planz0/src/static/images/tripply1.png"
    with open(logo_path, "rb") as logo_file:
        logo_data = logo_file.read()
stance, our dedicated customer support team is available to help. 
        Feel free to contact us at <a href="mailto:support@triply.co">support@triply.co</a>.</p>

        <p>Best Regards,<br>{from_name}</p>
    </body>
    </html>
    """

    # Dynamically set the sender display name and email
    dynamic_sender_email = f"{from_name} <{sender_email}>"
    
    # Create the email object
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=dynamic_sender_email, 
        to=[recipient_email]
    )
    email.content_subtype = "html"  # Set email content type to HTML

    # Attach the QR code to the email
    email.attach(qr_code_file.name, buffer.getvalue(), "image/png")

    # Send the email
    email.send(fail_silently=False)





@login_required
def eventEditView(request, id):
    profile = Profile.objects.get(user=request.user)
    event   = Event.objects.get(pk=id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home:eventDetail', id=id)
    else:
        form = EventEditForm(instance=event)

    template = loader.get_template('events/eventEdit.html')
    context = {
        'event'  : event,
        'profile': profile,
        'form'   : form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def eventDeleteView(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST': # If the request method is POST, delete the event
        event.delete()
        return redirect('profiles:profile')  
    
    template = loader.get_template('events/eventEdit.html')
    context = {
        'event'  : event,
              }
    return HttpResponse(template.render(context, request))

    profile = Profile.objects.get(user=request.user)  # Get the user's profile
    form    = EventCreationForm(request.POST or None, request.FILES or None)  # Create an instance of EventCreationForm with POST data if available, or None
    events  = Event.objects.all()  # Retrieve all events from the Event model
    if request.method == 'POST': 
        if form.is_valid():
            event = form.save(commit=False)  # Save form data to create a new event
            event.organizer = profile  # Assign the organizer of the event to the user's profile
            event.ksh = float(event.price) * 130.00  # Assuming some conversion for pricing
            event.save()
            event.attendees.add(profile)  # Add the user's profile as an attendee of the event

            # Set a flag in the session to indicate a successful event creation
            request.session['eventCreated'] = True

    template = loader.get_template('events/home.html')  # Load template
    context  = {
        "profile": profile,
        'form'   : form,
        'events' : events,
    }
    return HttpResponse(template.render(context, request))


@login_required
def eventDetailView(request, id):
    profile = Profile.objects.get(user=request.user)  # Get the profile from the request object
    event = Event.objects.get(pk=id)  # Get the event by ID

    profileEmail = profile.email  # Get the email address of the profile
    profileName = profile  # Get the name of the profile
    senderEmail = settings.DEFAULT_FROM_EMAIL  # Get the email address of the sender
    eventName = event.title  # Get the name of the event
    eventLocation = event.venue 
    uuid = generateUUID(profileEmail)
    profileSubject = f'Your tickets for: {eventName} at {eventLocation}'
    from_name = "Planz0"

    if request.method == 'POST': 
        if profile not in event.attendees.all():  # Check if the profile is not already in the list of event attendees
            sendUUID(profileSubject, profileName, senderEmail, profileEmail, uuid, event, from_name)  # Send an email with a unique UUID to the profile
            event.attendees.add(profile)  # Add the profile to the list of event attendees
            request.session['eventBooked'] = True  # Set a session variable indicating that the event has been booked

    template = loader.get_template('events/eventDetail.html')
    context = {
        'event': event,
        'profile': profile,
        'uuid': uuid,  
    }
    return HttpResponse(template.render(context, request))


# def sendUUID(subject, recipient_name, sender_email, recipient_email, uuid, event):
#     message = f"""
#     <html>
#     <body>
#     <p>Hi {recipient_name} 👋,</p>

#     <p>🎉 Your adventure is about to begin! We've reserved your spot for an incredible event, and we're thrilled to share the details with you.</p>

#     <p><strong>Event:</strong> {event.title}</p>
#     <p><strong>Date:</strong> {event.date}</p>

#     <p><strong>Your Secret Code:</strong> : {uuid}</p>

#     <p>Keep this code handy—it's your key to unlocking an unforgettable experience! 🗝️✨</p>

#     <p>We can't wait to see you there and make some amazing memories together!</p>

#     <p>Cheers,<br>The planzO Team 🚀</p>
#     </body>
#     </html>
#     """
#     send_mail(subject, message, f'planzO <{sender_email}>', [recipient_email], fail_silently=False, html_message=message)




def generateUUID(email):
    hashObject = hashlib.sha1(email.encode())  # Create a hash object and encode the email
    hexDigit = hashObject.hexdigest()  # Convert the hash to a hexadecimal string
    uuid = '-'.join([hexDigit[:3], hexDigit[3:6], hexDigit[6:9]])  # Customize UUID format
    return uuid


@login_required
def eventEditView(request, id):
    profile = Profile.objects.get(user=request.user)
    event   = Event.objects.get(pk=id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home:eventDetail', id=id)
    else:
        form = EventEditForm(instance=event)

    template = loader.get_template('events/eventEdit.html')
    context = {
        'event'  : event,
        'profile': profile,
        'form'   : form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def eventDeleteView(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':  # If the request method is POST, delete the event
        event.delete()
        return redirect('profiles:profile')

    template = loader.get_template('events/eventEdit.html')
    context = {
        'event': event,
    }
    return HttpResponse(template.render(context, request))