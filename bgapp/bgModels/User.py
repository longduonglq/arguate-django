from django.db import models
from .Topic import Topic
from .Conversation import Conversation
import uuid
import datetime

class User(models.Model):
    isOnline = models.BooleanField(default=True, editable=True)
    isBanned = models.BooleanField(default=False, editable=True)
    isActive = models.BooleanField(default=True, editable=True)

    isLooking = models.BooleanField(default=False, editable=True)
    topics = models.ManyToManyField(Topic, related_name='users')

    userID = models.UUIDField(editable=False, default=uuid.uuid4)


class UserOpinion(models.Model):
    timeStart = models.DateTimeField(editable=False, default=datetime.datetime.now)
    timeEnd = models.DateTimeField()
    isDeleted = models.BooleanField(default=False)

    position = models.BooleanField()
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='opinions')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='opinions')


class UserComplaint(models.Model):
    timeFiled = models.DateTimeField(default=datetime.datetime.now, editable=False)

    conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, related_name='complaints')
    filedBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='complaints_made')
    accused = models.ForeignKey(User, on_delete=models.PROTECT, related_name='complaints_received')

    complaintCode = models.CharField(max_length=5, default='')
    complaint = models.TextField()


class SessionInfo(models.Model):
    ip = models.GenericIPAddressField(null=True)

    timeStart = models.DateTimeField(editable=False, default=datetime.datetime.now)
    timeEnd = models.DateTimeField()

    user = models.ForeignKey('User', on_delete=models.PROTECT,
                             related_name='login_sessions')

    class Meta:
        ordering = ['-timeEnd']


class Ban(models.Model):
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    banType = models.CharField(max_length=5) # throttle or ban
    banCode = models.CharField(max_length=5, default='')
    reason = models.TextField()

    user = models.ForeignKey('User', on_delete=models.PROTECT,
                             related_name='bans')
