"""
ASGI config for batGround project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'batGround.settings')
django.setup()
application = get_default_application()

from bgapp.bgModels.User import User
for user in User.objects.all():
    user.channelID = None
