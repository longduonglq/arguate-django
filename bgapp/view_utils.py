from django.db import models
from bgapp.bgModels import Topic

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


options_per_page = 30
times_to_reset = 10
times = 0
cache = Topic.objects.annotate(num_convos=models.Count('conversations'))\
                                        .order_by('-num_convos')[:options_per_page]
def get_popular_topics():
    global times, cache
    if times < times_to_reset:
        times += 1
    else:
        times = 0
        cache = Topic.objects.annotate(num_convos=models.Count('conversations'))\
                                        .order_by('-num_convos')[:options_per_page]

    return cache