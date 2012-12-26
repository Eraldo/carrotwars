import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from rewards.models import Reward
from django.utils.safestring import mark_safe
from django.conf import settings

__author__ = "Eraldo Helal"

class PriceColumn(tables.Column):
    """
    Table column layout for displaying a price as carrot images.
    """

    def render(self, value):
        img_html = '<img src=%simages/carrot.png>' % settings.STATIC_URL
        if value <= 5:
            return mark_safe(img_html * value)
        else:
            return mark_safe('%s x %s' % (img_html, value))


class OwnedRewardTable(tables.Table):
    """
    Table layout for showing rewards owned by a user.
    """

    quester = tables.Column(accessor='relation.quester')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    price = PriceColumn()
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "price", "status")


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

    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    price = PriceColumn()
    buy = BuyColumn(accessor="pk")
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "buy")
        fields = ("title", "description", "price", "status")
