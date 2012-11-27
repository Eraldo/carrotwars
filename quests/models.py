from django.db import models
from relations.models import Relation

import datetime
from django.utils import timezone

class QuestManager(models.Manager):
    def get_relation_quests(self, relation):        
        return super(QuestManager, self).get_query_set().filter(relation=relation)
    def get_owned_quests(self, user):
        return super(QuestManager, self).get_query_set().filter(relation__owner=user)
    def get_assigned_quests(self, user):
        return super(QuestManager, self).get_query_set().filter(relation__quester=user)
    def get_all_quests(self, user):
        return super(QuestManager, self).get_query_set()
    
class Quest(models.Model):
    relation = models.ForeignKey(Relation)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    activation_date = models.DateTimeField(blank=True, null=True)
    RATINGS = (
        (1, '*\tconsider it done'),
        (2, '**\tsounds easy'),
        (3, '***\tI will give it a try'),
        (4, '****\tsounds challenging'),
        (5, '*****\tI will do my best'),
    )
    rating = models.PositiveSmallIntegerField(default=1, max_length=1, choices=RATINGS)
    STATUS = (
        ('C', 'created'),
        ('A', 'accepted'),
        ('M', 'marked complete'),
        ('D', 'done'),
        ('F', 'failed'),
    )
    status = models.CharField(default='C', max_length=1, choices=STATUS)
    quests = QuestManager()

    def __unicode__(self):
        return self.title

    def is_active(self):
        "Returns True if this quest is active."
        return self.status in ('A')

    def set_active(self):
        self.activation_date = timezone.now()
        self.status = 'A'

    # class Meta:
    #     verbose_name_plural = "quests"
