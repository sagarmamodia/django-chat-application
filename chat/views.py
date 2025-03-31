import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django_chat_app import settings

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from PIL import Image

@login_required(login_url='/login')
def home(request):
    return redirect('/lobby')

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse("You are already logged in.")
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse("Incorrect username or password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/lobby')
        else:
            return HttpResponse("Incorrect username or password")

    return render(request, 'chat/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        #check if email is already in database
        if User.objects.filter(username=username).count() == 0:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('/login')
        else:
            return HttpResponse("Account with the same username already exists.")

    return render(request, 'chat/register.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def lobby(request):
    user = User.objects.get(id=request.user.id)
    distinct_users = User.objects.all().distinct()

    active_chats = []

    for other_user in distinct_users:
        if user.id==other_user.id or other_user.username=="root":
            continue
        
        last_message = Message.objects.filter(
            (Q(sender=user) & Q(receiver=other_user)) | 
            (Q(sender=other_user) & Q(receiver=user))
        ).first()

        if last_message is not None:
            last_message_text = last_message.body
        else:
            last_message_text = "no message..."
        
        active_chats.append({
            "user_id":other_user.id,
            "username":other_user.username,
            "last_message": last_message_text,
            "profile_icon": static('images/default_profile_icon.png')
        })
        

    context = {'active_chats':active_chats}
    return render(request, 'chat/lobby.html', context=context)

@login_required(login_url='/login')
def chat_page(request, receiver_username):
    user = User.objects.get(id=request.user.id)
    receiver_user = User.objects.get(username=receiver_username)

    chat_messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=receiver_user)) | 
            (Q(sender=receiver_user) & Q(receiver=user))
        ).order_by("created")
    
    
    context = {'sender_username': user.username, 
               'receiver_username':receiver_username, 
               'chat_messages': chat_messages, 
               'delete_icon_url': static('images/delete_icon.png'), 
               'edit_icon_url': static('images/edit_icon.png'),
               'media_url': settings.MEDIA_URL
               }
    return render(request, 'chat/chat.html', context=context)

@login_required(login_url='/login')
def delete_message(request, receiver_username, pk):
    if request.method == "GET":
        message = Message.objects.get(id=pk)
        if message is not None:
            message.delete()

    return redirect('chat-page', receiver_username=receiver_username)

@login_required(login_url='/login')
def upload_file(request, receiver_username):
    if request.method == 'POST':
        file = request.FILES['toUploadFile']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(file_path):
            with open(file_path, "wb+") as img:
                img.write(file.read())
        
        sender = User.objects.get(username=request.user.username)
        receiver = User.objects.get(username=receiver_username)
        file_url = os.path.join(settings.MEDIA_URL, file.name)
        created_message = Message.objects.create(sender=sender, receiver=receiver, message_type="image", body=file_url)
    
        chat_group_name = ""
        if request.user.username > receiver_username:
            chat_group_name = request.user.username + receiver_username
        else:
            chat_group_name = receiver_username + request.user.username
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            chat_group_name, 
            {"type": "chat.message", 
             "id": created_message.id,  
             "sender_username": request.user.username, 
             "message_type": created_message.message_type, 
             "message_text": created_message.body}
        )

    return redirect('chat-page', receiver_username=receiver_username)
