import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.other_user = self.scope['url_route']['kwargs']['other_user']
        self.user = self.scope['user']
        
        if self.user.username > self.other_user:
            self.chat_group_name = self.user.username + self.other_user
        else:
            self.chat_group_name = self.other_user + self.user.username
        
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )        
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )
    
    def receive(self, text_data):
        text_parsed_data = json.loads(text_data)
        message = text_parsed_data["message"]
        sender = User.objects.get(username=self.user.username)
        receiver = User.objects.get(username=self.other_user)
        Message.objects.create(sender=sender, receiver=receiver, body=message)

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, {"type": "chat.message", "sender": self.user.username, "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        if event['sender'] != self.user.username:
            self.send(text_data=json.dumps({"message": message}))