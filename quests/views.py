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
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import datetime, timedelta
from django_tables2 import RequestConfig

from django.forms.widgets import RadioSelect

__author__ = "Eraldo Helal"

class QuestForm(ModelForm):
    quester = forms.ModelChoiceField(queryset = User.objects.all())
    CHOICES = (('1', 'First',), ('2', 'Second',))

    class Meta:
        model = Quest
        exclude = ('relation', 'activation_date', 'deadline', 'status',)
        widgets = {
            'rating': RadioSelect(attrs={'class':'star required'}),
        }

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class QuestMixin(LoginRequiredMixin):
    model = Quest
    form_class = QuestForm
    
    def get_context_data(self, **kwargs):
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
    pass

class QuestDetailView(QuestMixin, DetailView):
    pass

class QuestCreateView(QuestMixin, CreateView):
    success_url = '.' # reverse('quests:list')

    def get_form(self, form_class):
        form = super(QuestCreateView, self).get_form(form_class)
        owned_relations = Relation.objects.owned_by(self.request.user)
        form.fields['quester'].queryset = User.objects.filter(pk__in=owned_relations.values('quester'))
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.relation = Relation.objects.get(owner=self.request.user, quester=form.cleaned_data['quester'])
        self.object.save()
        self.inform_user()
        messages.add_message(self.request, messages.INFO, 'New quest has been created. Waiting for Quester to accept.')
        return super(QuestCreateView, self).form_valid(form)

    def inform_user(self):
        subject = "New quest!"
        body = """<a href="%s">%s</a>""" % (self.object.get_absolute_url(), self.object.title)
        pm_write(
            sender=self.request.user,
            recipient=self.object.relation.quester,
            subject=subject,
            body=body
            )

class QuestDeleteView(QuestMixin, DeleteView):
    pass

class QuestUpdateView(QuestMixin, UpdateView):
    pass

class AcceptView(RedirectView):
    def get_redirect_url(self, pk):
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.quester or quest.status != 'C':
            return reverse('quests:list')

        # update quest
        quest.status = 'A'
        quest.activation_date = datetime.now()
        quest.deadline = datetime.now()+timedelta(days=7)
        quest.save()
        
        messages.add_message(self.request, messages.INFO, 'Quest has been accepted.')
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.owner,
            subject="Quest %s has been accepted." % quest.title,
            body=""
            )
        return reverse('quests:list')


class DeclineView(RedirectView):
    def get_redirect_url(self, pk):
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.quester or quest.status != 'C':
            return reverse('quests:list')

        # update quest
        quest.status = 'R'
        quest.save()
        
        messages.add_message(self.request, messages.INFO, 'Quest has been declined.')
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.owner,
            subject="Quest %s has been declined." % quest.title,
            body=""
            )
        return reverse('quests:list')


class CompleteView(RedirectView):
    def get_redirect_url(self, pk):
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.quester or quest.status != 'A':
            return reverse('quests:list')

        # update quest
        quest.status = 'M'
        quest.save()
        
        messages.add_message(self.request, messages.INFO, 'Quest has been marked as completed. Owner has been informed.')
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.owner,
            subject="Quest %s has been marked as completed." % quest.title,
            body=""
            )
        return reverse('quests:list')


class ConfirmView(RedirectView):
    def get_redirect_url(self, pk):
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

        messages.add_message(self.request, messages.INFO, 'Quest completion has been confirmed. %s earned %s carrot%s.' % (quest.relation.quester, quest.rating, "s"[quest.rating==1:]))
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.quester,
        subject="Quest %s completion has been confirmed. You earned %s carrot%s!" % (quest.title, quest.rating, "s"[quest.rating==1:]),
            body=""
            )
        return reverse('quests:list')


class DenyView(RedirectView):
    def get_redirect_url(self, pk):
        quest = Quest.objects.get(pk=pk)

        # check permission
        if self.request.user != quest.relation.owner or quest.status != 'M':
            return reverse('quests:list')

        # update quest
        quest.status = 'A'
        quest.save()

        messages.add_message(self.request, messages.INFO, 'Quest completion has been denied.')
        pm_write(
            sender=self.request.user,
            recipient=quest.relation.quester,
            subject="Quest %s completion has been denied." % quest.title,
            body=""
            )
        return reverse('quests:list')
