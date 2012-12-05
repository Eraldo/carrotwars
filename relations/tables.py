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

class PendingRelationTable(tables.Table):
    owner = tables.LinkColumn('relations:detail', args=[A('pk')])
    accept = tables.BooleanColumn()
    decline = tables.BooleanColumn()
    
    class Meta:
        model = Relation
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        # sequence = ("owner", "description", "...", "owner")
        fields = ("owner",)
