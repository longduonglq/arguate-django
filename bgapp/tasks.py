from __future__ import absolute_import, unicode_literals
from batGround.celery import app

from django.db import models
from bgapp.bgModels.User import Topic

@app.task
def mark_users_offline_after():
    pass
