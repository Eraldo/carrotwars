#!/usr/bin/env python
"""
Contains the django admin interface settings related to the relation model.
"""

from django.contrib import admin
from relations.models import Relation
from quests.models import Quest
from rewards.models import Reward

__author__ = "Eraldo Helal"


class QuestInline(admin.TabularInline):
    """Meta information model to display Quests inline."""
    model = Quest
    extra = 0

class RewardInline(admin.TabularInline):
    """Meta information model to display Rewards inline."""
    model = Reward
    extra = 0

class RelationAdmin(admin.ModelAdmin):
    """
    Meta information model to display Relations
    with associated inline Quests and Rewards.
    """
    inlines = [QuestInline, RewardInline]

admin.site.register(Relation, RelationAdmin)
