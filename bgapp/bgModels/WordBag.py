from django.db import models

class WordBag(models.Model):
    opposite_bag = models.OneToOneField('WordBag', on_delete=models.SET_NULL, null=True)

def make_synonyms(topics):
    pass

def make_antonyms(topics):
    pass
