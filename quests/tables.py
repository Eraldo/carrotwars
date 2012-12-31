import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from quests.models import Quest
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime, timedelta

__author__ = "Eraldo Helal"


class UserColumn(tables.TemplateColumn):
    """
    Table column layout for avatar and username display of a user.
    """
        
    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <span id="center-text">
        <a href="{% url 'relations:detail' record.relation.pk %}">
          <img id="avatar" src="{{ MEDIA_URL }}{{ value.profile.avatar }}">
          {{ value }}
        </a>
        </span>
        """ 
        super(UserColumn, self).__init__(*args, **kwargs)


class RatingColumn(tables.Column):
    """
    Table column layout for displaying a rating as carrot images.
    """

    def render(self, value):
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        if len(value) <= 5:
            return mark_safe(img_html * len(value))
        else:
            return mark_safe('%s x %s' % (img_html, len(value)))


class DeadlineColumn(tables.Column):
    """
    Table column layout for displaying a color coded deadline.
    """

    def render(self, value):
        today = datetime.now().date()
        deadline = value.date()
        # render date in color depending on time left
        if today == deadline: # due
            return mark_safe('<span id="due">%s</span>' % value.date())
        elif today < deadline: # not due
            return mark_safe('<span id="notdue">%s</span>' % value.date())
        else: # over due
            return mark_safe('<span id="overdue">%s</span>' % value.date())

class OwnedQuestTable(tables.Table):
    """
    Table layout for showing quests owned by a user.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    deadline = DeadlineColumn()
    rating = RatingColumn()
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "deadline", "rating")


class CompleteColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as completed.
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:complete' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/complete.png" />
            </form>
            """ 
        super(CompleteColumn, self).__init__(*args, **kwargs)
        

class AssignedQuestTable(tables.Table):
    """
    Table layout for showing quests assigned to a user.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    deadline = DeadlineColumn()
    complete = CompleteColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "deadline", "complete")
        fields = ("title", "description", "deadline", "rating")
        

class AcceptColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as accepted.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:accept' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/accept.png" />
            </form>
            """ 
        super(AcceptColumn, self).__init__(*args, **kwargs)

class DeclineColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as declined.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:decline' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/decline.png" />
            </form>
            """ 
        super(DeclineColumn, self).__init__(*args, **kwargs)


class PendingQuestTable(tables.Table):
    """
    Table layout for showing quests pending for a user.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    accept = AcceptColumn(accessor="pk", orderable=False)
    decline = DeclineColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "accept", "decline")
        fields = ("title", "description", "rating")


class ConfirmColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as confirmed.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:confirm' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/confirm.png" />
            </form>
            """ 
        super(ConfirmColumn, self).__init__(*args, **kwargs)

class DenyColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as denied.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:deny' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/deny.png" />
            </form>
            """ 
        super(DenyColumn, self).__init__(*args, **kwargs)
        

class CompletedQuestTable(tables.Table):
    """
    Table layout for showing quests completed for a user.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    confirm = ConfirmColumn(accessor="pk", orderable=False)
    deny = DenyColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester", "confirm", "deny")
        fields = ("title", "description", "rating")


class WaitingQuestTable(tables.Table):
    """
    Table layout for showing quests a user is waiting for.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner")
        fields = ("title", "description", "rating")


class ProposedQuestTable(tables.Table):
    """
    Table layout for showing quests a user is waiting for.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "rating")
