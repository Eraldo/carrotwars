#!/usr/bin/env python
"""
Contains the table settings for the quest model.
"""

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from quests.models import Quest
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime, timedelta

__author__ = "Eraldo Helal"


class UserColumn(tables.Column):
    """
    Table column layout for avatar and username display of a user.
    """

    def render(self, value, record):
        """Returns a html string version representing a user."""
        user = value
        quest = record
        if user == quest.relation.owner:
            return quest.relation.get_owner_html
        elif user == quest.relation.quester:
            return quest.relation.get_quester_html


class DescriptionColumn(tables.Column):
    """
    Table column layout for displaying a description.
    If the description is long.. a shortened version will be used.
    """

    def render(self, value, record):
        """Returns a html string version representing a description."""
        max_lenth = 60
        if len(value) > max_lenth:
            html = value[:max_lenth] + " .."
        else:
            html = value
        return html
  

class RatingColumn(tables.Column):
    """
    Table column layout for displaying a rating as carrot images.
    """

    def render(self, value, record):
      """Returns the html string version of the record rating."""
      return record.get_rating_html()


class DeadlineColumn(tables.Column):
    """
    Table column layout for displaying a color coded deadline.
    """

    def render(self, value, record):
        """Returns a html string version representing the records deadline."""
        return record.get_deadline_html()
    

class OwnedQuestTable(tables.Table):
    """
    Table layout for showing quests owned by a user.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    description = DescriptionColumn()
    deadline = DeadlineColumn()
    rating = RatingColumn()
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "deadline", "rating")


class CompleteColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as completed.
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:complete' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/complete.png" />
            </form>
            """ 
        super(CompleteColumn, self).__init__(*args, **kwargs)
        

class AssignedQuestTable(tables.Table):
    """
    Table layout for showing quests assigned to a user.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    description = DescriptionColumn()
    rating = RatingColumn()
    deadline = DeadlineColumn()
    complete = CompleteColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "deadline", "complete")
        fields = ("title", "description", "deadline", "rating")
        

class AcceptColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as accepted.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:accept' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/accept.png" />
            </form>
            """ 
        super(AcceptColumn, self).__init__(*args, **kwargs)

class DeclineColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as declined.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:decline' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/decline.png" />
            </form>
            """ 
        super(DeclineColumn, self).__init__(*args, **kwargs)


class PendingQuestTable(tables.Table):
    """
    Table layout for showing quests pending for a user.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    description = DescriptionColumn()
    rating = RatingColumn()
    accept = AcceptColumn(accessor="pk", orderable=False)
    decline = DeclineColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner", "accept", "decline")
        fields = ("title", "description", "rating")


class ConfirmColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as confirmed.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:confirm' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Accept" src="/static/images/confirm.png" />
            </form>
            """ 
        super(ConfirmColumn, self).__init__(*args, **kwargs)

class DenyColumn(tables.TemplateColumn):
    """
    Table column layout for marking a quest as denied.
    """

    def __init__(self, *args, **kwargs):
        kwargs['template_code'] = """
        {% load url from future %}
        <form action="{% url 'quests:deny' value %}" method="POST">
            {% csrf_token %}
            <input type="image" value="Decline" src="/static/images/deny.png" />
            </form>
            """ 
        super(DenyColumn, self).__init__(*args, **kwargs)
        

class CompletedQuestTable(tables.Table):
    """
    Table layout for showing quests completed for a user.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    description = DescriptionColumn()
    rating = RatingColumn()
    confirm = ConfirmColumn(accessor="pk", orderable=False)
    deny = DenyColumn(accessor="pk", orderable=False)
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester", "confirm", "deny")
        fields = ("title", "description", "rating")


class WaitingQuestTable(tables.Table):
    """
    Table layout for showing quests a user is waiting for.
    """

    owner = UserColumn(accessor='relation.owner')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    description = DescriptionColumn()
    rating = RatingColumn()
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "owner")
        fields = ("title", "description", "rating")


class ProposedQuestTable(tables.Table):
    """
    Table layout for showing quests proposed for a user.
    """

    quester = UserColumn(accessor='relation.quester')
    title = tables.LinkColumn('quests:detail', args=[A('pk')])
    description = DescriptionColumn()
    rating = RatingColumn()
    
    class Meta:
        model = Quest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("title", "description", "...", "quester")
        fields = ("title", "description", "rating")
