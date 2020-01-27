from django.db import models
from .Topic import Topic
import uuid
from django.utils import timezone

class Conversation(models.Model):
    timeStart = models.DateTimeField(default=timezone.now)
    timeEnd = models.DateTimeField()
    isEnded = models.BooleanField(default=False, editable=True)

    conversation_id = models.UUIDField(editable=False, default=uuid.uuid4)
    users = models.ManyToManyField('User', related_name='conversations')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='conversations')


class Message(models.Model):
    timeSent = models.DateTimeField(default=timezone.now, editable=False)

    content = models.TextField()
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE,
                                     related_name='messages')

    sender = models.ForeignKey('User', on_delete=models.PROTECT,
                               related_name='sentMessages')

    receiver = models.ForeignKey('User', on_delete=models.PROTECT,
                                 related_name='receivedMessages')

    class Meta:
        ordering = ['-timeSent']