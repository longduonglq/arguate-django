# this contains code to generate test db
from bgapp.bgModels import *
from django.db import models
import random
from random import randint
import datetime
import uuid

random.seed(1)

def generate_users(num):
    for i in range(num):
        user = User.objects.create()
        for sess_num in range(random.randint(0, 50)):
            SessionInfo.objects.create(
                ip='192.254.4.35',
                timeEnd=datetime.datetime.now() + datetime.timedelta(hours=random.randint(0, 24)),
                user=user,
            )
        print('user: {}'.format(user.userID))

def generate_topics(num):
    for i in range(num):
        content = 'content-'+ str(uuid.uuid4())
        topic = Topic.objects.create(
            userStarted=User.objects.all()[randint(0, User.objects.count() - 1)],
            content=content
        )
        pc = ProCamp.objects.create(topic=topic)
        cc = ConCamp.objects.create(topic=topic)

        print('topic: {}'.format(content))

def simulate_users_choosing_topics():
    for user in User.objects.all():
        for topic in Topic.objects.all():
            skip = random.choice([True, False])
            if skip:
                continue

            user.topics.add(topic)
            opinion = random.choice([True, False])
            if opinion:
                topic.pro_camp.users.add(user)
            else:
                topic.con_camp.users.add(user)

def simulate():
    generate_users(1000)
    generate_topics(10)
    simulate_users_choosing_topics()

def update_topic_camp_user_count():
    for topic in Topic.objects.all():
        topic.pro_camp.user_count = topic.pro_camp.users.count()
        topic.pro_camp.save()

        topic.con_camp.user_count = topic.con_camp.users.count()
        topic.con_camp.save()