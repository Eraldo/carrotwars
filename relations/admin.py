from django.contrib import admin
from relations.models import Relation
from quests.models import Quest
from rewards.models import Reward

class QuestInline(admin.TabularInline):
    model = Quest
    extra = 0

class RewardInline(admin.TabularInline):
    model = Reward
    extra = 0

class RelationAdmin(admin.ModelAdmin):
    inlines = [QuestInline, RewardInline]

admin.site.register(Relation, RelationAdmin)
