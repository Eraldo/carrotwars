#!/usr/bin/env python
"""db model representing a relation of two users"""

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

__author__ = "Eraldo Helal"
    
class RelationManager(models.Manager):
    """
    Provides easy access to pre-defined custom relation filters.
    """

    def owned_by(self, user):
        """Returns the set of relations owned by the provided user."""
        return super(RelationManager, self).get_query_set().filter(owner=user, status='A')
    def assigned_to(self, user):
        """Returns the set of relations assigned to the provided user."""
        return super(RelationManager, self).get_query_set().filter(quester=user, status='A')
    def proposed_by(self, user):
        """Returns the set of relations proposed by the provided user."""
        return super(RelationManager, self).get_query_set().filter(owner=user).filter(status='C')
    
    def pending_for(self, user):
        """Returns the set of relations pensing for the provided user."""
        return super(RelationManager, self).get_query_set().filter(quester=user, status='C')

class Relation(models.Model):

    owner = models.ForeignKey(User, related_name='relation_owner')
    quester = models.ForeignKey(User, related_name='relation_quester')
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    balance = models.IntegerField(default=0, help_text="Amount of credits the quester has.")
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

    def get_balance_html(self):
        balance = self.balance
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        html = ""
        if balance == 0:
            html = "no credits"
        elif balance <= 5:
            html = img_html * balance
        else:
            html = '%s x %s' % (img_html, balance)
        return mark_safe(html)

    def _get_user_html(self, user):
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        link = reverse('relations:detail', args=[self.pk])
        template = """
        <span id="center-text">
        <a id="user-link" href="%s">
          %s %s
        </a>
        </span>
        """ % (link, self._get_user_image_html(user, "icon"), user)
        html = ""
        if user:
            html = template
        return mark_safe(html)

    def get_owner_html(self):
        return self._get_user_html(self.owner)

    def get_quester_html(self):
        return self._get_user_html(self.quester)

    def _get_user_image_html(self, user, id):
        # return # TODO return image
        image_path = user.profile.avatar
        img_html = '<img id="%s" src="%s%s">' % (id, settings.MEDIA_URL, image_path)
        html = ""
        if image_path:
            html = img_html
        return mark_safe(html)

    def get_owner_image_html(self):
        return self._get_user_image_html(self.owner, "image")

    def get_quester_image_html(self):
        return self._get_user_image_html(self.quester, "image")

    def get_owner_icon_html(self):
        return self._get_user_image_html(self.owner, "icon")

    def get_quester_icon_html(self):
        return self._get_user_image_html(self.quester, "icon")

