import re
from django.db import models

import random
from random import shuffle
random.seed(1)

def get_opponent(opinion_list):
    opinion_list = opinion_list.filter(isDeleted=False)

    random_range = list(range(opinion_list.count()))
    shuffle(random_range)
    for index in random_range:
        if opinion_list[index].position:
            opponents = opinion_list[index].topic.con_camp.users.filter(
                                                            isBanned=False,
                                                            isLooking=True)
        else:
            opponents = opinion_list[index].topic.pro_camp.users.filter(
                                                            isBanned=False,
                                                            isLooking=True)

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

