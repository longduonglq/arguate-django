# Generated by Django 3.0.1 on 2020-01-12 19:03

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bgapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='conversation_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='timeStart',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='user',
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='feedbacks', to='bgapp.User'),
        ),
        migrations.AlterField(
            model_name='message',
            name='timeSent',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name='sessioninfo',
            name='timeStart',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='dateStart',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='userID',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='usercomplaint',
            name='timeFiled',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name='useropinion',
            name='timeStart',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.DeleteModel(
            name='Error',
        ),
    ]
