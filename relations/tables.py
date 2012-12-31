import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from relations.models import Relation
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse

__author__ = "Eraldo Helal"


class UserColumn(tables.TemplateColumn):
    """
    Table column layout for avatar and username display of a user.
    """
        
    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <span id="center-text">
        <a href="{% url 'relations:detail' record.pk %}">
          <img id="avatar" src="{{ MEDIA_URL }}{{ value.profile.avatar }}">
          {{ value }}
        </a>
        </span>
        """ 
        super(UserColumn, self).__init__(*args, **kwargs)


class BalanceColumn(tables.Column):
    """
    Table column layout for displaying a relations balance as carrot images.
    """

    def render(self, value, record):
        return record.get_balance_html


class OwnedRelationTable(tables.Table):
    """
    Table layout for showing relations owned by a user.
    """
        
    quester = UserColumn()
    balance = BalanceColumn()
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("title", "description", "...", "quester")
        fields = ("quester", "balance")

class AssignedRelationTable(tables.Table):
    """
    Table layout for showing relations assigned to a user.
    """
    
    owner = UserColumn()
    balance = BalanceColumn()
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner", "balance")

class AcceptColumn(tables.TemplateColumn):
    """
    Table column layout for marking a relation as accepted.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'relations:accept' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/accept.png" />
            </form>
            """ 
        super(AcceptColumn, self).__init__(*args, **kwargs)

class DeclineColumn(tables.TemplateColumn):
    """
    Table column layout for marking a relation as declined.
    """
        
    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'relations:decline' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/decline.png" />
            </form>
            """ 
        super(DeclineColumn, self).__init__(*args, **kwargs)

class PendingRelationTable(tables.Table):
    """
    Table layout for showing relations pending for a user.
    """
    owner = UserColumn()
    accept = AcceptColumn(accessor="pk", orderable=False)
    decline = DeclineColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner",)


class ProposedRelationTable(tables.Table):
    """
    Table layout for showing relations proposed by a user.
    """

    quester = UserColumn()
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("quester",)
