from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class RelationManager(models.Manager):
    def owned_by(self, user):
        return super(RelationManager, self).get_query_set().filter(owner=user)
    def assigned_to(self, user):
        return super(RelationManager, self).get_query_set().filter(quester=user)
    def pending_for(self, user):
        return super(RelationManager, self).get_query_set().filter(quester=user, status='C')

class Relation(models.Model):
    owner = models.ForeignKey(User, related_name='relation_owner')
    quester = models.ForeignKey(User, related_name='relation_quester')
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    balance = models.IntegerField(default=0)
    STATUS = (
        ('C', 'created'),
        ('A', 'accepted'),
        ('R', 'declined'),
        ('X', 'deleted'),
    )
    status = models.CharField(default='C', max_length=1, choices=STATUS)
    objects = RelationManager()
    
    def __unicode__(self):
        return u'%s - %s' % (self.owner, self.quester)

    def get_absolute_url(self):
        return reverse('relations:detail', args=[self.pk])
    
    class Meta:
        unique_together = ("owner", "quester")
