from django.db import models
from django.contrib.auth.models import User

class RelationManager(models.Manager):
    def owned(self, user):
        return super(RelationManager, self).get_query_set().filter(owner=user)
    def assigned(self, user):
        return super(RelationManager, self).get_query_set().filter(quester=user)

class Relation(models.Model):
    owner = models.ForeignKey(User, related_name='relation_owner')
    quester = models.ForeignKey(User, related_name='relation_quester')
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    balance = models.IntegerField(default=0)
    STATUS = (
        ('C', 'created'),
        ('A', 'accepted'),
    )
    status = models.CharField(default='C', max_length=1, choices=STATUS)
    objects = RelationManager()
    
    def __unicode__(self):
        return u'%s - %s' % (self.owner, self.quester)
    
    class Meta:
        unique_together = ("owner", "quester")
