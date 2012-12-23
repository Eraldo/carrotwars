import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from rewards.models import Reward

class OwnedRewardTable(tables.Table):
    quester = tables.Column(accessor='relation.quester')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "price", "status")


class BuyColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'rewards:buy' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Buy" src="/static/images/accept.gif" />
            </form>
            """ 
        super(BuyColumn, self).__init__(*args, **kwargs)


class AssignedRewardTable(tables.Table):
    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    buy = BuyColumn(accessor="pk")
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "buy")
        fields = ("title", "description", "price", "status")
