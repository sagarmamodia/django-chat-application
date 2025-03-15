from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('lobby/', views.lobby, name='lobby'),
    path('chat/<str:receiver_username>/', views.chat_page, name='chat-page'),
]