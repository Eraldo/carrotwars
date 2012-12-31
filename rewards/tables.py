import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from rewards.models import Reward
from django.utils.safestring import mark_safe
from django.conf import settings

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
