from django.db import models
from relations.models import Relation
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from postman.api import pm_write

__author__ = "Eraldo Helal"

class QuestManager(models.Manager):
    """
    Provides easy access to pre-defined custom quest filters.
    """
    
    def for_relation(self, relation):
        """Returns the set of quests associated to the provided relation."""
        return super(QuestManager, self).get_query_set().filter(relation=relation, status='A')
    def owned_by(self, user):
        """Returns the set of quests owned by the provided user."""
        return super(QuestManager, self).get_query_set().filter(relation__owner=user, status='A')
    def assigned_to(self, user):
        """Returns the set of quests assigned to the provided user."""
        return super(QuestManager, self).get_query_set().filter(relation__quester=user, status='A')
    def proposed_by(self, user):
        """Returns the set of quests proposed by the provided user."""
        return super(QuestManager, self).get_query_set().filter(relation__owner=user).filter(status='C')
    def pending_for(self, user):
        """Returns the set of quests pending for the provided user."""
        return super(QuestManager, self).get_query_set().filter(relation__quester=user).filter(status='C')
    def completed_for(self, user):
        """Returns the set of quests completed by the provided user."""
        return super(QuestManager, self).get_query_set().filter(relation__owner=user).filter(status='M')
    def waiting_for(self, user):
        """Returns the set of quests the provided user is waiting for."""
        return super(QuestManager, self).get_query_set().filter(relation__quester=user).filter(status='M')

    def update_status(self):
        """Checks all quests to see if they are overdue and fails them if so."""
        quests = super(QuestManager, self).get_query_set()
        for quest in quests:
            if quest.status == 'A' and quest.is_overdue():
                quest.fail()

    
class Quest(models.Model):

    relation = models.ForeignKey(Relation)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    activation_date = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    RATINGS = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )
    rating = models.PositiveSmallIntegerField(default=1, max_length=1, choices=RATINGS)
    bomb = models.BooleanField()
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

    def activate(self):
        self.status = 'A'
        self.activation_date = timezone.now()
        self.deadline = timezone.now()+timedelta(days=7)

    def is_overdue(self):
        today = timezone.now().date()
        deadline = self.deadline
        if deadline and today > deadline.date():
            return True
        else:
            return False

    def fail(self):
        deduction = 0
        if self.bomb:
            if self.relation.balance >= self.rating:
                self.relation.balance -= self.rating
                self.relation.save()
                deduction = self.rating
            else:
                defuction = self.relation.balance
        self.status = 'F'
        self.save()
        # notify owner
        pm_write(
            sender=self.relation.quester,
            recipient=self.relation.owner,
            subject="Quest %s has failed. %s lost %s carrot%s." % (
                self.title, self.relation.quester.title(), deduction, "s"[deduction==1:]),
            body=""
            )
        # notify quester
        pm_write(
            sender=self.relation.owner,
            recipient=self.relation.quester,
            subject="Quest %s has failed. You lost %s carrot%s." % (self.title, deduction, "s"[deduction==1:]),
            body=""
            )
        # TODO notify both owner and quester?
        # TODO no loss message for non-bomb quests
    
    def get_deadline_html(self):
        if not self.deadline:
            return "-"
        today = timezone.now().date()
        deadline = self.deadline.date()
        warning_days = 1
        template = '<span id="deadline-%s">%s</span>'
        html = ""
        # render date in color depending on time left
        if today == deadline: # due
            html = template % ("due", deadline)
        elif today < deadline: # not yet due
            if (deadline - today).days <= warning_days: # soon due
                html = template % ("soon-due", deadline)
            else: # not due
                html = template % ("not-due", deadline)
        else: # over due
            html = template % ("over-due", deadline)
        return  mark_safe(html)

    def get_rating_html(self):
        rating = self.rating
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        html = ""
        if rating <= 5:
            html = img_html * rating
        else:
            html = '%s x %s' % (img_html, rating)
        if self.bomb:
            html += " " + self.get_bomb_html()
        return mark_safe(html)

    def get_bomb_html(self):
        bomb = self.bomb
        img_html = '<img src=%simages/bomb.png>' % settings.STATIC_URL
        html = ""
        if bomb:
            html = img_html
        return mark_safe(html)

    def get_description_html(self):
        if self.description:
            return self.description
        else:
            return "-"

