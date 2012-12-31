import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from rewards.models import Reward
from django.utils.safestring import mark_safe
from django.conf import settings

__author__ = "Eraldo Helal"


class UserColumn(tables.Column):
    """
    Table column layout for avatar and username display of a user.
    """

    def render(self, value, record):
        user = value
        quest = record
        if user == quest.relation.owner:
            return quest.relation.get_owner_html
        elif user == quest.relation.quester:
            return quest.relation.get_quester_html


class PriceColumn(tables.Column):
    """
    Table column layout for displaying a price as carrot images.
    """

    def render(self, value, record):
        return record.get_price_html


class OwnedRewardTable(tables.Table):
    """
    Table layout for showing rewards owned by a user.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    price = PriceColumn()
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "price")


class BuyColumn(tables.TemplateColumn):
    """
    Table column layout for marking a reward as bought.
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'rewards:buy' value %}" method="POST">
            {% csrf_token %}
            {% if record.price <= record.relation.balance %}
              <input type="image" value="Buy" src="/static/images/buy.png" />
            {% else %}
              <input type="image" value="Buy" src="/static/images/buy-inactive.png" />
            {% endif %}
            </form>
            """ 
        super(BuyColumn, self).__init__(*args, **kwargs)


class AssignedRewardTable(tables.Table):
    """
    Table layout for showing rewards assigned to a user.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    price = PriceColumn()
    buy = BuyColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "buy")
        fields = ("title", "description", "price")
