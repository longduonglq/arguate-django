# Generated by Django 3.0.2 on 2020-01-31 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activity',
            field=models.TextField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='user',
            name='channelID',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]