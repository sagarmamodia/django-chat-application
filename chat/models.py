from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="message_sent", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="message_received", on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.body