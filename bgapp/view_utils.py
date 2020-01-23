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
def memoized_func(times):
    class mfunc:
        def __init__(self, f):
            self.f = f
            self.limit = times
            self.curTime = 0
            self.cache = {}

        def __call__(self, *args):
            key = hash(args)
            if self.curTime < self.limit:
                self.curTime += 1
                if key not in self.cache:
                    self.cache[key] = self.f(*args)
                return self.cache[key]

            else:
                self.curTime = 0
                self.cache = {key: self.f(*args)}
                return self.cache[key]

    return mfunc


options_per_page = 30
@memoized_func(5)
def get_popular_topics():
    return Topic.objects.annotate(
            num_convos=models.Count('conversations', filter=models.Q(conversations__isEnded=False) )
    ).order_by('-num_convos')[:options_per_page]


# used to sort search result based on similarity to string entered
memoized_str_dist = functools.lru_cache(maxsize=None)(jellyfish.jaro_winkler)

