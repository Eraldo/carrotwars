from django.db import models
from relations.models import Relation

import datetime
from django.utils import timezone

class RewardManager(models.Manager):
    def get_relation_rewards(self, relation):        
        return super(RewardManager, self).get_query_set().filter(relation=relation)
    def get_owned_rewards(self, user):
        return super(RewardManager, self).get_query_set().filter(relation__owner=user)
    def get_offered_rewards(self, user):
        return super(RewardManager, self).get_query_set().filter(relation__quester=user)
    def get_all_rewards(self, user):
        return super(RewardManager, self).get_query_set()

class Reward(models.Model):
    relation = models.ForeignKey(Relation)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    price = models.IntegerField(default=1)
    STATUS = (
        ('C', 'created'),
        ('A', 'accepted'),
        ('M', 'marked bought'),
        ('B', 'bought'),
    )
    status = models.CharField(default='C', max_length=1, choices=STATUS)
    rewards = RewardManager()

    def __unicode__(self):
        return self.title

    def is_active(self):
        return self.status in ('A')

    def set_active(self):
        self.activation_date = timezone.now()
        self.status = 'A'

    # class Meta:
    #     verbose_name_plural = "rewards"
