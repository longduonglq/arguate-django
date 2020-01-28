# Generated by Django 3.0.2 on 2020-01-27 21:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bgapp', '0008_auto_20200126_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='timeStart',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='message',
            name='timeSent',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='sessioninfo',
            name='timeStart',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='dateStart',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='usercomplaint',
            name='timeFiled',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='useropinion',
            name='timeStart',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.CreateModel(
            name='ChannelID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channelID', models.TextField()),
            ],
            options={
                'unique_together': {('channelID',)},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='channelID',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='bgapp.ChannelID'),
        ),
    ]
