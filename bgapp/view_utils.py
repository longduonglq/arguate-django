from django.db import models
from bgapp.bgModels import Topic
import jellyfish
import functools

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

# empty the cache after n call, only take positional argument
def memoized_times(times):
    class mfunc:
        def __init__(self, f):
            self.f = f
            self.limit = times
            self.curTime = {}
            self.cache = {}

        def __call__(self, *args):
            key = hash(args)
            if key not in self.curTime:
                self.curTime[key] = 0

            if self.curTime[key] < self.limit:
                self.curTime[key] += 1
                if key not in self.cache:
                    self.cache[key] = self.f(*args)
                return self.cache[key]

            else:
                self.curTime[key] = 0
                self.cache[key] = self.f(*args)
                return self.cache[key]

    return mfunc


options_per_page = 30
@memoized_times(1)
def get_popular_topics():
    return Topic.objects.annotate(
            num_convos=models.Count('conversations', filter=models.Q(conversations__isEnded=False) )
    ).order_by('-num_convos')[:options_per_page]


# used to sort search result based on similarity to string entered
memoized_str_dist = functools.lru_cache(maxsize=None)(jellyfish.jaro_winkler)


@memoized_times(5)
def get_topic_suggestions(user_input):
    # user input should already been stripped
    kws = user_input.split(' ')
    q_obj = models.Q(content__icontains=kws[0])
    for kw in kws[1:]:
        q_obj = q_obj | models.Q(content__icontains=kw)

    topic_suggestions = [e for e in Topic.objects.filter(q_obj)]
    topic_suggestions.sort(
        key=lambda x: memoized_str_dist(x.content, user_input.strip()),
        reverse=True
    )
    return topic_suggestions

