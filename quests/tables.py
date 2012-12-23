import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from quests.models import Quest
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.urlresolvers import reverse

class OwnedQuestTable(tables.Table):
    quester = tables.Column(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "rating", "status")


class CompleteColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:complete' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/accept.gif" />
            </form>
            """ 
        super(CompleteColumn, self).__init__(*args, **kwargs)
        

class AssignedQuestTable(tables.Table):
    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    complete = CompleteColumn(accessor="pk")
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "complete")
        fields = ("title", "description", "rating", "status")
        

class AcceptColumn(tables.TemplateColumn):

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

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:decline' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/decline.gif" />
            </form>
            """ 
        super(DeclineColumn, self).__init__(*args, **kwargs)

    # def render(self, value):
    #     url = reverse('quests:decline', kwargs={'pk': value})
    #     return mark_safe('<a href="%s"><img src="/static/images/decline.gif" /></a>' % escape(url))


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
        fields = ("title", "description", "rating")


class ConfirmColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:confirm' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/accept.gif" />
            </form>
            """ 
        super(ConfirmColumn, self).__init__(*args, **kwargs)

class DenyColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:deny' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/decline.gif" />
            </form>
            """ 
        super(DenyColumn, self).__init__(*args, **kwargs)
        

class CompletedQuestTable(tables.Table):
    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    confirm = ConfirmColumn(accessor="pk")
    deny = DenyColumn(accessor="pk")
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "confirm", "deny")
        fields = ("title", "description", "rating")
