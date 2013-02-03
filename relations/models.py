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
    Provides easy access to pre-defined custom relation sets.
    (using django filters)
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
        """Returns the set of relations pending for the provided user."""
        return super(RelationManager, self).get_query_set().filter(quester=user, status='C')

class Relation(models.Model):
    """
    A django model representing a persistant 1-to-1 relation between two users.
    Including a credit balance showing how many credits a quester has gained from the owner.
    """

    owner = models.ForeignKey(User, related_name='relation_owner') # creator of the relation
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
    objects = RelationManager() # custom django quest manager
    
    def __unicode__(self):
        """Returns the unicode string representation of the relation."""
        return u'%s - %s' % (self.owner, self.quester)

    def get_absolute_url(self):
        """Returns the absolute url of the relation."""
        return reverse('relations:detail', args=[self.pk])
    
    class Meta:
        #: Constraint making sure that each relation is unique.
        unique_together = ("owner", "quester")

    def get_balance_html(self):
        """
        Returns the html representation of the relation balance as a string.
        The code displays a string if balance is 0,
        1-5 carrot images if below 6
        or single carrot image, a times symbol and a number representing
        the amount of collected carrots if above 5.
        """
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
        """Returns the html reperesentation of a user containing avatar and username as a string."""
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        link = reverse('relations:detail', args=[self.pk])
        template = """
        <a id="user-link" href="%s">
          %s<span id="user-link-text">%s</span>
        </a>
        """ % (link, self._get_user_image_html(user, "icon"), user)
        html = ""
        if user:
            html = template
        return mark_safe(html)

    def get_owner_html(self):
        """Returns the html reperesentation of the relation owner containing avatar and username as a string."""
        return self._get_user_html(self.owner)

    def get_quester_html(self):
        """Returns the html reperesentation of the relation quester containing avatar and username as a string."""
        return self._get_user_html(self.quester)

    def _get_user_image_html(self, user, id):
        """Returns the html reperesentation of a user avatar as a string."""
        image_path = user.profile.avatar
        img_html = '<img id="%s" src="%s%s">' % (id, settings.MEDIA_URL, image_path)
        html = ""
        if image_path:
            html = img_html
        return mark_safe(html)

    def get_owner_image_html(self):
        """Returns the html reperesentation the relation owner avatar as a string."""
        return self._get_user_image_html(self.owner, "image")

    def get_quester_image_html(self):
        """Returns the html reperesentation the relation quester avatar as a string."""
        return self._get_user_image_html(self.quester, "image")

    def get_owner_icon_html(self):
        """Returns the html reperesentation the relation owner avatar icon as a string."""
        return self._get_user_image_html(self.owner, "icon")

    def get_quester_icon_html(self):
        """Returns the html reperesentation the relation quester avatar icon as a string."""
        return self._get_user_image_html(self.quester, "icon")

