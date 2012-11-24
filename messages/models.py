from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title

    def is_active(self):
        return self.active
