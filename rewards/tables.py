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

class AssignedRewardTable(tables.Table):
    owner = tables.Column(accessor='relation.owner')
    title = tables.LinkColumn('rewards:detail', args=[A('pk')])
    
    class Meta:
        model = Reward
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner")
        fields = ("title", "description", "price", "status")
