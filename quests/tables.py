import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from quests.models import Quest
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.conf import settings

class RatingColumn(tables.Column):
    """
    Table column layout for displaying a rating as carrot images.
    """

    def render(self, value):
        img_html = '<img src=%simages/carrot-25.png>' % settings.STATIC_URL
        if len(value) <= 5:
            return mark_safe(img_html * len(value))
        else:
            return mark_safe('%s x %s' % (img_html, len(value)))


class OwnedQuestTable(tables.Table):
    """
    Table layout for showing quests owned by a user.
    """
    quester = tables.Column(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()

    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "rating")


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

    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    deadline = tables.DateColumn()
    complete = CompleteColumn(accessor="pk")
    
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
            <input type="image" value="Accept" src="/static/images/accept.gif" />
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
            <input type="image" value="Decline" src="/static/images/decline.gif" />
            </form>
            """ 
        super(DeclineColumn, self).__init__(*args, **kwargs)


class PendingQuestTable(tables.Table):
    """
    Table layout for showing quests pending for a user.
    """

    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    accept = AcceptColumn(accessor="pk")
    decline = DeclineColumn(accessor="pk")
    
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
            <input type="image" value="Accept" src="/static/images/confirm.gif" />
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
            <input type="image" value="Decline" src="/static/images/deny.gif" />
            </form>
            """ 
        super(DenyColumn, self).__init__(*args, **kwargs)
        

class CompletedQuestTable(tables.Table):
    """
    Table layout for showing quests completed for a user.
    """

    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    rating = RatingColumn()
    confirm = ConfirmColumn(accessor="pk")
    deny = DenyColumn(accessor="pk")
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "confirm", "deny")
        fields = ("title", "description", "rating")
