from django.db import models
from bgapp.bgModels import Topic
from .GConfig import GConfig
import jellyfish
from datetime import datetime, timedelta
from cachetools import LFUCache, cached
from .cache import *

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


options_per_page = GConfig.Topic.options_per_page
@memoized_times(GConfig.Topic.popularTopic_MT)
def get_popular_topics():
    return Topic.objects \
        .filter(isHidden=False) \
        .annotate(
            num_convo=models.Count(
                'conversations',
                conversations__timeStart__gte=datetime.now()
                + timedelta(days=GConfig.Topic.popularTopicLast_Days)
            )
        ) \
        .order_by('-num_convo')[:options_per_page]


# used to sort search result based on similarity to string entered
memoized_str_dist = cached(cache={}, key=lambda x, y: frozenset([x, y])) \
                            (jellyfish.jaro_distance)


@memoized_times(GConfig.Topic.userTopic_MT)
def get_topic_suggestions(user_input):
    # user input should already been stripped
    kws = user_input.split(' ')
    q_obj = models.Q(content__icontains=kws[0])
    for kw in kws[1:]:
        q_obj = q_obj | models.Q(content__icontains=kw)

    topic_suggestions = [
        e for e in Topic.objects.filter(q_obj, isHidden=False)
    ]
    topic_suggestions.sort(
        key=lambda x: memoized_str_dist(x.content, user_input.strip()),
        reverse=True
    )
    return topic_suggestions

