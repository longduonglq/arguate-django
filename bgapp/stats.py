from prometheus_client import Summary, Gauge, Counter, Histogram
from numpy import arange

# summary of views
get_topics_Latency = Histogram('get_topics_Latency', 'Latency of get_topics')
get_user_topics_Latency = Histogram('get_user_topics_Latency', 'Latency to return user topics')

# summary of consumers
online_user_Num = Gauge('online_user_Num', 'Number of users online')
online_user_Num.set(0)
new_users_Num = Counter('new_users_Num', 'Number of newly created users')
active_user_Num = Gauge('active_user_Num', 'Number of user active in last 30 days')

active_convo_Num = Gauge('active_convo_Num', 'Number of active conversation')
active_convo_Num.set(0)
new_convo_Num = Counter('new_convo_Num', 'Number of new convo')

topics_created = Counter('topics_created', 'Number of new topics created')
active_topics_num = Gauge('active_topics_num', 'Number of current topics')

opinions_registered = Counter('opinions_registered', 'num of opinions registered')
active_opinion_num = Gauge('active_opinion_num', 'active opinion num')
# chat related tracker
start_chat_Wait = Histogram(
    'start_chat_Wait', 'Wait time to start a convo',
    buckets=list(arange(0, 16, 1)) # in seconds
)
conversation_duration = Histogram(
    'conversation_duration', 'Conversation duration',
    buckets=list(arange(0.5, 30, 0.5)) # in minutes
)
session_duration = Histogram(
    'session_duration', 'Session duration',
    buckets=list(arange(0.5, 30, 0.5))
)

found_fail = Counter('found_fail', 'chat finding',
                     ['status'])
# general
#ws_request_time =
