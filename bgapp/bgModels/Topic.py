from django.db import models
from ..cache import memoized_times
from ..GConfig import GConfig
import uuid
from django.utils import timezone

class Topic(models.Model):
    dateStart = models.DateTimeField(editable=False, default=timezone.now)
    userStarted = models.ForeignKey('User', on_delete=models.PROTECT, related_name='topics_started')

    content = models.TextField(editable=True)
    topic_id = models.UUIDField(editable=False, default=uuid.uuid4)
    isHidden = models.BooleanField(editable=True, default=False)

    synonyms = models.ManyToManyField('self', blank=True, null=True)
    antonyms = models.ManyToManyField('self', blank=True, null=True)

    # override save() instead of __init__
    def save(self, *args, **kwargs):
        if not self.pk:
            # if this is the first time a topic is created
            # then create associated ProCamp and ConCamp
            super(Topic, self).save(*args, **kwargs)
            ProCamp.objects.create(topic=self)
            ConCamp.objects.create(topic=self)
            return None
        super(Topic, self).save(*args, **kwargs)

    def camp(self, camp):
        if camp:
            return self.pro_camp
        else:
            return self.con_camp

    def nym(self, bool):
        if bool:
            return self.synonyms
        else:
            return self.antonyms

    def get_all_nyms(self, bnym):
        # if nyms is True get all synonyms and vice versa
        result = set([])
        visited = {}
        for topic in Topic.objects.all():
            visited[topic] = False

        queue = []
        visited[self] = True
        queue.append(self)

        topic = queue.pop(0)
        for nym in topic.nym(bnym).all():
            visited[nym] = True
            queue.append(nym)
            result.add(nym)

        while queue:
            topic = queue.pop(0)
            for nym in topic.nym(True).all():
                if not visited[nym]:
                    visited[nym] = True
                    queue.append(nym)
                    result.add(nym)

        return result

    def __str__(self):
        return str(self.content)

class ProCamp(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, related_name='pro_camp')
    users = models.ManyToManyField('User', related_name='pro_camps')

    @property
    @memoized_times(GConfig.Cache.camp_userCount_MT)
    def user_count(self):
        return self.users.count()


class ConCamp(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, related_name='con_camp')
    users = models.ManyToManyField('User', related_name='con_camps')

    @property
    @memoized_times(GConfig.Cache.camp_userCount_MT)
    def user_count(self):
        return self.users.count()

