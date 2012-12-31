from django.db import models
from relations.models import Relation
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

import datetime
from django.utils import timezone

__author__ = "Eraldo Helal"

class RewardManager(models.Manager):
    """
    Provides easy access to pre-defined custom reward filters.
    """

    def for_relation(self, relation):
        """Returns the set of rewards associated to the provided relation."""
        return super(RewardManager, self).get_query_set().filter(relation=relation, status='A')
    def owned_by(self, user):
        """Returns the set of rewards owned by the provided user."""
        return super(RewardManager, self).get_query_set().filter(relation__owner=user, status='A')
    def assigned_to(self, user):
        """Returns the set of rewards assigned to the provided user."""
        return super(RewardManager, self).get_query_set().filter(relation__quester=user, status='A')

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
        ('D', 'bought'),
        ('X', 'deleted'),
    )
    status = models.CharField(default='A', max_length=1, choices=STATUS)
    objects = RewardManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rewards:detail', args=[self.pk])
    
    def is_active(self):
        return self.status in ('A')

    def set_active(self):
        self.activation_date = timezone.now()
        self.status = 'A'

    def get_price_html(self):
        price = self.price
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        html = ""
        if price == 0:
            html = "free"
        elif price <= 5:
            html = img_html * price
        else:
            html = '%s x %s' % (img_html, price)
        return mark_safe(html)
