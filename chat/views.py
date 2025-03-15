from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return redirect('/signin')

def signin(request):
    
    if request.user.is_authenticated:
        return HttpResponse("You are already signed in.")
    
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

    return render(request, 'chat/signin.html')

def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check if email is already in database
        if User.objects.filter(username=username).count() == 0:
            User.objects.create(username=username, email=email, password=password)
            return redirect('/signin')
        else:
            return HttpResponse("Account with the same username already exists.")

    return render(request, 'chat/signup.html')

def signout(request):
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
            "profile_icon": '#'
        })
        

    context = {'active_chats':active_chats}
    return render(request, 'chat/lobby.html', context=context)

@login_required(login_url='signin')
def chat_page(request, username):
    user = User.objects.get(id=request.user.id)
    other_user = User.objects.get(username=username)

    chat_messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=other_user)) | 
            (Q(sender=other_user) & Q(receiver=user))
        ).order_by("created")
    
    
    context = {'username':username, 'chat_messages': chat_messages}
    return render(request, 'chat/chat.html', context=context)