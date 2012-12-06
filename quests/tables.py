import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from quests.models import Quest

class OwnedQuestTable(tables.Table):
    quester = tables.Column(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "rating", "status")

class AssignedQuestTable(tables.Table):
    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner")
        fields = ("title", "description", "rating", "status")

from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.urlresolvers import reverse
class AcceptColumn(tables.Column):
    def render(self, value):
        url = reverse('quests:accept', kwargs={'pk': value})
        return mark_safe('<a href="%s"><img src="/static/images/accept.gif" /></a>' % escape(url))
class DeclineColumn(tables.Column):
    def render(self, value):
        url = reverse('quests:decline', kwargs={'pk': value})
        return mark_safe('<a href="%s"><img src="/static/images/decline.gif" /></a>' % escape(url))

class PendingQuestTable(tables.Table):
    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    accept = AcceptColumn(accessor="pk")
    decline = DeclineColumn(accessor="pk")
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "accept", "decline")
        fields = ("title", "description", "rating", "id")
