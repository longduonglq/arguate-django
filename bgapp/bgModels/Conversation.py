from django.db import models
from .Topic import Topic
import uuid
import datetime

class Conversation(models.Model):
    timeStart = models.DateTimeField(default=datetime.datetime.now, editable=False)
    timeEnd = models.DateTimeField()
    isEnded = models.BooleanField(default=False, editable=True)

    conversation_id = models.UUIDField(editable=False, default=uuid.uuid4)
    users = models.ManyToManyField('User', related_name='conversations')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='conversations')


class Message(models.Model):
    timeSent = models.DateTimeField(default=datetime.datetime.now, editable=False)

    content = models.TextField()
    conversation = models.ForeignKey('Conversation', on_delete=models.PROTECT,
                                     related_name='messages')

    sender = models.ForeignKey('User', on_delete=models.PROTECT,
                               related_name='sentMessages')

    receiver = models.ForeignKey('User', on_delete=models.PROTECT,
                                 related_name='receivedMessages')

    class Meta:
        ordering = ['-timeSent']