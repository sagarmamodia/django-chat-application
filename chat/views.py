from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

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

        #check if email is already in database
        if User.objects.filter(username=username).count() == 0:
            User.objects.create(username=username, email=email, password=password)
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
               }
    return render(request, 'chat/chat.html', context=context)

@login_required(login_url='/login')
def delete_message(request, receiver_username, pk):
    if request.method == "GET":
        message = Message.objects.get(id=pk)
        if message is not None:
            message.delete()

    return redirect('chat-page', receiver_username=receiver_username)
    