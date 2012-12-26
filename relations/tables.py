import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from relations.models import Relation
from django.utils.safestring import mark_safe
from django.conf import settings

__author__ = "Eraldo Helal"

class BalanceColumn(tables.Column):
    """
    Table column layout for displaying a relations balance as carrot images.
    """

    def render(self, value):
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        if value <= 5:
            return mark_safe(img_html * value)
        else:
            return mark_safe('%s x %s' % (img_html, value))


class OwnedRelationTable(tables.Table):
    """
    Table layout for showing relations owned by a user.
    """
        
    quester = tables.LinkColumn('relations:detail', args=[A('pk')])
    balance = BalanceColumn()
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("title", "description", "...", "quester")
        fields = ("quester", "balance", "status")

class AssignedRelationTable(tables.Table):
    """
    Table layout for showing relations assigned to a user.
    """
    
    owner = tables.LinkColumn('relations:detail', args=[A('pk')])
    balance = BalanceColumn()
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner", "balance", "status")

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
    owner = tables.LinkColumn('relations:detail', args=[A('pk')])
    accept = AcceptColumn(accessor="pk")
    decline = DeclineColumn(accessor="pk")
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner",)
