from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('lobby/', views.lobby, name='lobby'),
    path('chat/<str:receiver_username>/', views.chat_page, name='chat-page'),
    path('chat/<str:receiver_username>/delete/<int:pk>/', views.delete_message, name='delete-message'),
    path('chat/<str:receiver_username>/upload/', views.upload_file, name='upload-file'),
    path('file/<str:filename>/', views.serve_image, name='serve-image'),
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)