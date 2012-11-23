from django.db import models
from django.contrib.auth.models import User

class Relation(models.Model):
    owner = models.ForeignKey(User, related_name='relation_owner')
    quester = models.ForeignKey(User, related_name='relation_quester')
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    balance = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s - %s' % (self.owner, self.quester)
    
    class Meta:
        #verbose_name_plural = "relations"
        unique_together = ("owner", "quester")
