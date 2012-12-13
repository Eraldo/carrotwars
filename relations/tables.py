import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from relations.models import Relation

class OwnedRelationTable(tables.Table):
    quester = tables.LinkColumn('relations:detail', args=[A('pk')])
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("title", "description", "...", "quester")
        fields = ("quester", "balance", "status")

class AssignedRelationTable(tables.Table):
    owner = tables.LinkColumn('relations:detail', args=[A('pk')])
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner", "balance", "status")

class AcceptColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'relations:accept' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/accept.gif" />
            </form>
            """ 
        super(AcceptColumn, self).__init__(*args, **kwargs)

class DeclineColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'relations:decline' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/decline.gif" />
            </form>
            """ 
        super(DeclineColumn, self).__init__(*args, **kwargs)

class PendingRelationTable(tables.Table):
    owner = tables.LinkColumn('relations:detail', args=[A('pk')])
    accept = AcceptColumn(accessor="pk")
    decline = DeclineColumn(accessor="pk")
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner",)
