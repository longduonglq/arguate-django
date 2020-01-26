from __future__ import absolute_import, unicode_literals
from batGround.celery import app
from datetime import datetime, timedelta

from django.db import models
from bgapp.bgModels import User, Topic
from .stats import *
from .GConfig import GConfig
from .stats import active_user_Num, active_topics_num

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        GConfig.User.markUserInactiveTimeCycle * 60,
        mark_users_inactive_after.s(),
        name='mark user inactive every timecycle minutes'
    )

    sender.add_periodic_task(
        GConfig.User.markUserOfflineTimeCycle * 60,
        mark_users_offline_after.s(),
        name='mark user offline every timecycle minutes'
    )

    sender.add_periodic_task(
        #GConfig.Topic.recountTopicAfterModerated * 60,
        1,
        count_current_topic.s(),
        name='count current topic every timecycle minutes'
    )

@app.task
def mark_users_offline_after():
    for user in User.objects.filter(isOnline=True).all():
        if user.login_sessions[0].timeEnd < \
                datetime.now() + timedelta(days=-GConfig.User.markUserOfflineAfter):
            user.isOnline = False


@app.task
def mark_users_inactive_after():
    # mark user inactive after 30 days
    for user in User.objects.filter(isActive=True).all():
        if user.login_sessions[0].timeEnd < \
                datetime.now() + timedelta(days=-GConfig.User.markUserInactiveAfter):
            user.isActive = False

    active_user_Num.set(User.objects.filter(isActive=True).count())


@app.task
def count_current_topic():
    # count current topics after moderated
    active_topics_num.set(Topic.objects.count())
