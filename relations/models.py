from django.db import models
from django.contrib.auth.models import User

class RelationManager(models.Manager):
    def get_owned_relations(self, user):
        return super(RelationManager, self).get_query_set().filter(owner=user)
    def get_assigned_relations(self, user):
        return super(RelationManager, self).get_query_set().filter(quester=user)
    def get_all_relations(self):
        return super(RelationManager, self).get_query_set()

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
    relations = RelationManager()
    
    def __unicode__(self):
        return u'%s - %s' % (self.owner, self.quester)
    
    class Meta:
        #verbose_name_plural = "relations"
        unique_together = ("owner", "quester")
