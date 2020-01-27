import random
from random import shuffle
random.seed(1)

def get_opponent(opinion_list):
    opinion_list = opinion_list.filter(isDeleted=False)

    random_range = list(range(opinion_list.count()))
    shuffle(random_range)
    for index in random_range:
        opponents = opinion_list[index] \
                    .topic \
                    .camp(not opinion_list[index].position) \
                    .users \
                    .filter(
                        isBanned=False,
                        isLooking=True
                    )

        opponents_count = opponents.count()
        if opponents_count > 0:
            return opponents[random.randint(0, opponents_count - 1)], opinion_list[index]
        else:
            continue

    return 'NOT_FOUND', None

def msg_security_check(msg):
    return msg, True

def topic_security_check(topic):
    return topic, True

def getMinutes(td):
    return (td.seconds//60) % 60

class IncrementalAverage:
    book = {} # stat, [avg, N]

    @staticmethod
    def add_to_average(stat, value):
        if stat not in IncrementalAverage.book:
            IncrementalAverage.book[stat] = [0, 0]

        avg, N = IncrementalAverage.book[stat]
        IncrementalAverage.book[stat] = [(avg * N + value)/(N + 1), N + 1]
        return IncrementalAverage.book[stat][0]

    @staticmethod
    def get_avg(stat):
        return IncrementalAverage.book[stat][0]
