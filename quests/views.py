from quests.models import Quest
from relations.models import Relation
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quests.tables import OwnedQuestTable, AssignedQuestTable, PendingQuestTable
from postman.api import pm_write
from django.core.urlresolvers import reverse
from django.contrib import messages

class QuestForm(ModelForm):
    quester = forms.ModelChoiceField(queryset = User.objects.all())
    
    # def __init__(self, user=None, **kwargs):
    #     super(QuestForm, self).__init__(**kwargs)
    #     if user:
    #         self.fields['relation'].queryset = Relation.objects.filter(owner=user)

    class Meta:
        model = Quest
        exclude = ('relation', 'activation_date', 'status',)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class QuestMixin(LoginRequiredMixin):
    model = Quest
    form_class = QuestForm
    
    def get_context_data(self, **kwargs):
        context = super(QuestMixin, self).get_context_data(**kwargs)
        context['owned'] = Quest.objects.owned_by(self.request.user)
        context['assigned'] = Quest.objects.assigned_to(self.request.user)
        context['pending'] = Quest.objects.pending_for(self.request.user)
        context['owned_table'] = OwnedQuestTable(context['owned'])
        context['assigned_table'] = AssignedQuestTable(context['assigned'])
        context['pending_table'] = PendingQuestTable(context['pending'])
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
        quest.status = 'A'
        quest.save()
        messages.add_message(self.request, messages.INFO, 'Quest has been accepted.')
        return reverse('quests:list')

class DeclineView(RedirectView):
    def get_redirect_url(self, pk):
        quest = Quest.objects.get(pk=pk)
        quest.status = 'R'
        quest.save()
        messages.add_message(self.request, messages.INFO, 'Quest has been declined.')
        return reverse('quests:list')
