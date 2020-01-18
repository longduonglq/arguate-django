from .User import User
from django.db import models

class Feedback(models.Model):
    reviewed = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='feedbacks', on_delete=models.PROTECT, null=True)
    email = models.CharField(max_length=40)
    feedback = models.TextField()
