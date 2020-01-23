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
