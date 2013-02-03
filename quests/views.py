#!/usr/bin/env python
"""
This module contains the quest model based views.
"""

from quests.models import Quest
from relations.models import Relation
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quests.tables import OwnedQuestTable, AssignedQuestTable, PendingQuestTable, CompletedQuestTable, WaitingQuestTable, ProposedQuestTable
from postman.api import pm_write
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import datetime, timedelta
from django_tables2 import RequestConfig

from django.forms.widgets import RadioSelect

__author__ = "Eraldo Helal"


class QuestForm(ModelForm):
    """
    A basic quest form.
    (django form)
    """
    quester = forms.ModelChoiceField(queryset = User.objects.all())

    class Meta:
        model = Quest
        exclude = ('relation', 'activation_date', 'deadline', 'status',)
        widgets = {
            'rating': RadioSelect(attrs={'class':'star required'}),
        }


class LoginRequiredMixin(object):
    """
    A mixin class to enforce login.
    If the user is not logged in,
    he will be redirected to the login page.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Processes the request and redirects to login page if not logged in."""
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class QuestMixin(LoginRequiredMixin):
    """
    Mixin class that sets main context information that is needed for quest object views.
    Configures quest set filters, table information and default quest form.
    """
    model = Quest
    form_class = QuestForm
    
    def get_context_data(self, **kwargs):
        """
        Configures quest set filters and table information.
        Returns a context dictionary.
        """
        context = super(QuestMixin, self).get_context_data(**kwargs)
        context['owner'] = Relation.objects.owned_by(self.request.user)
        context['owned'] = Quest.objects.owned_by(self.request.user)
        context['assigned'] = Quest.objects.assigned_to(self.request.user)
        context['proposed'] = Quest.objects.proposed_by(self.request.user)
        context['pending'] = Quest.objects.pending_for(self.request.user)
        context['completed'] = Quest.objects.completed_for(self.request.user)
        context['waiting'] = Quest.objects.waiting_for(self.request.user)
        context['owned_table'] = OwnedQuestTable(context['owned'])
        context['assigned_table'] = AssignedQuestTable(context['assigned'])
        context['proposed_table'] = ProposedQuestTable(context['proposed'])
        context['pending_table'] = PendingQuestTable(context['pending'])
        context['completed_table'] = CompletedQuestTable(context['completed'])
        context['waiting_table'] = WaitingQuestTable(context['waiting'])
        requestConfig = RequestConfig(self.request, paginate={"per_page": 10,})
        requestConfig.configure(context['owned_table'])
        requestConfig.configure(context['assigned_table'])
        requestConfig.configure(context['proposed_table'])
        requestConfig.configure(context['pending_table'])
        requestConfig.configure(context['completed_table'])
        requestConfig.configure(context['waiting_table'])
        return context


class QuestListView(QuestMixin, ListView):
    """A generic view providing context information for lists of quests."""


class QuestDetailView(QuestMixin, DetailView):
    """A generic view providing context information for a single quest."""


class QuestCreateView(QuestMixin, CreateView):
    """
    A generic view providing context information and functionality for quest creation.
    """
    success_url = '.' # reverse('quests:list')

    def get_form(self, form_class):
        """
        Gets the default quest creation form and filters the quester choices
        to a list of users that already are in a quester role with respect
        to the current user.
        Returns the html form as a string.
        """
        form = super(QuestCreateView, self).get_form(form_class)
        owned_relations = Relation.objects.owned_by(self.request.user)
        form.fields['quester'].queryset = User.objects.filter(pk__in=owned_relations.values('quester'))
        return form

    def form_valid(self, form):
        """
        Validates the posted form data,
        sets the current user to be the quest owner
        and informs the new quester if successful.
        Returns True if successful - False otherwise.
        """
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.relation = Relation.objects.get(owner=self.request.user, quester=form.cleaned_data['quester'])

        if self.object.bomb:
            self.object.activate()
            success_msg = 'New quest has been created.'
        else:
            success_msg = 'New quest has been created. Waiting for Quester to accept.'

        self.object.save()
        
        self.inform_user()
        messages.add_message(self.request, messages.INFO, success_msg)

        return super(QuestCreateView, self).form_valid(form)

    def inform_user(self):
        """
        Informs the quester of the newly created quest.
        """
        subject = "New quest!"
        body = """<a href="%s">%s</a>""" % (self.object.get_absolute_url(), strip_tags(self.object.title))
        pm_write(
            sender=self.request.user,
            recipient=self.object.relation.quester,
            subject=subject,
            body=body
            )


class QuestDeleteView(QuestMixin, DeleteView):
    """A generic view providing context information for single quest deletion."""


class QuestUpdateView(QuestMixin, UpdateView):
    """A generic view providing context information for updating a single quest."""


class AcceptView(RedirectView):
    """
    A generic view providing context information and functionality
    for accepting a single quest.
    """
    def get_redirect_url(self, pk):
        """
        Checks if the current user has permission to accept the quest.
        Accepts the quest and informs the owner if successful.
        Returns the redirect URL as a string.
        """
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.quester or quest.status != 'C':
            return reverse('quests:list')

        # update quest
        quest.activate()
        quest.save()

        # inform owner
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.owner,
            subject="Quest %s has been accepted." % quest.title,
            body=""
            )

        messages.add_message(self.request, messages.SUCCESS, 'Quest has been accepted.')
        return reverse('quests:list')


class DeclineView(RedirectView):
    """
    A generic view providing context information and functionality
    for declining a single quest.
    """
    def get_redirect_url(self, pk):
        """
        Checks if the current user has permission to decline the quest.
        Declines the quest and informs the owner if successful.
        Returns the redirect URL as a string.
        """
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.quester or quest.status != 'C':
            return reverse('quests:list')

        # update quest
        quest.status = 'R'
        quest.save()

        # inform owner
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.owner,
            subject="Quest %s has been declined." % quest.title,
            body=""
            )

        messages.add_message(self.request, messages.INFO, 'Quest has been declined.')
        return reverse('quests:list')


class CompleteView(RedirectView):
    """
    A generic view providing context information and functionality
    for completing a single quest.
    """
    def get_redirect_url(self, pk):
        """
        Checks if the current user has permission to complete the quest.
        Completes the quest and informs the owner if successful.
        Returns the redirect URL as a string.
        """
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.quester or quest.status != 'A':
            return reverse('quests:list')

        # update quest
        quest.status = 'M'
        quest.save()

        # inform owner
        messages.add_message(self.request, messages.INFO, 'Quest has been marked as completed. Owner has been informed.')
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.owner,
            subject="Quest %s has been marked as completed." % quest.title,
            body=""
            )
        return reverse('quests:list')


class ConfirmView(RedirectView):
    """
    A generic view providing context information and functionality
    for confirming that a single quest has been completed.
    """
    def get_redirect_url(self, pk):
        """
        Checks if the current user has permission to confirm the quest completion.
        Confirms the quest completion and informs and credits the quester if successful.
        Returns the redirect URL as a string.
        """
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.owner or quest.status != 'M':
            return reverse('quests:list')

        # update quest
        quest.status = 'D'
        quest.save()
        
        # update balance
        relation = Relation.objects.get(owner=self.request.user, quester=quest.relation.quester)
        relation.balance += quest.rating
        relation.save()

        # inform quester
        messages.add_message(self.request, messages.INFO, 'Quest completion has been confirmed. %s earned %s carrot%s.' % (quest.relation.quester, quest.rating, "s"[quest.rating==1:]))
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.quester,
        subject="Quest %s completion has been confirmed. You earned %s carrot%s!" % (quest.title, quest.rating, "s"[quest.rating==1:]),
            body=""
            )
        return reverse('quests:list')


class DenyView(RedirectView):
    """
    A generic view providing context information and functionality
    for denying that a single quest has been completed.
    """
    def get_redirect_url(self, pk):
        """
        Checks if the current user has permission to deny the quest completion.
        Denies the quest completion and informs the quester if successful.
        Returns the redirect URL as a string.
        """
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.owner or quest.status != 'M':
            return reverse('quests:list')

        # update quest
        quest.status = 'A'
        quest.save()

        # inform quester
        messages.add_message(self.request, messages.INFO, 'Quest completion has been denied.')
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.quester,
            subject="Quest %s completion has been denied." % quest.title,
            body=""
            )
        return reverse('quests:list')
