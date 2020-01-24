from django.db import models
from .WordBag import WordBag
from ..cache import memoized_times
import uuid
import datetime

class Topic(models.Model):
    dateStart = models.DateTimeField(editable=False, default=datetime.datetime.now)
    userStarted = models.ForeignKey('User', on_delete=models.PROTECT, related_name='topics_started')

    content = models.TextField()
    topic_id = models.UUIDField(editable=False, default=uuid.uuid4)

    wordbag = models.ForeignKey(WordBag, on_delete=models.PROTECT, related_name='words', null=True)

class ProCamp(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.PROTECT, related_name='pro_camp')
    users = models.ManyToManyField('User', related_name='pro_camps')

    @property
    @memoized_times(1)
    def user_count(self):
        return self.users.count()

class ConCamp(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.PROTECT, related_name='con_camp')
    users = models.ManyToManyField('User', related_name='con_camps')

    @property
    @memoized_times(1)
    def user_count(self):
        return self.users.count()