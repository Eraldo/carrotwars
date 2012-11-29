import django_tables2 as tables
from quests.models import Quest

class QuestTable(tables.Table):
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
