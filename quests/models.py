from django.db import models
from relations.models import Relation
from django.core.urlresolvers import reverse

import datetime
from django.utils import timezone

class QuestManager(models.Manager):
    def for_relation(self, relation):        
        return super(QuestManager, self).get_query_set().filter(relation=relation, status='A')
    def owned_by(self, user):
        return super(QuestManager, self).get_query_set().filter(relation__owner=user, status='A')
    def assigned_to(self, user):
        return super(QuestManager, self).get_query_set().filter(relation__quester=user, status='A')
    def pending_for(self, user):
        return super(QuestManager, self).get_query_set().filter(relation__quester=user).filter(status='C')
    
class Quest(models.Model):
    relation = models.ForeignKey(Relation)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    activation_date = models.DateTimeField(blank=True, null=True)
    RATINGS = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )
    rating = models.PositiveSmallIntegerField(default=1, max_length=1, choices=RATINGS)
    STATUS = (
        ('C', 'created'),
        ('A', 'accepted'),
        ('R', 'declined'),
        ('M', 'marked complete'),
        ('D', 'done'),
        ('F', 'failed'),
        ('X', 'deleted'),
    )
    status = models.CharField(default='C', max_length=1, choices=STATUS)
    objects = QuestManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quests:detail', args=[self.pk])

    def is_active(self):
        "Returns True if this quest is active."
        return self.status in ('A')

    def set_active(self):
        self.activation_date = timezone.now()
        self.status = 'A'

