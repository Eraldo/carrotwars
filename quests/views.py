from quests.models import Quest
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quests.tables import OwnedQuestTable, AssignedQuestTable, PendingQuestTable
from postman.api import pm_write

class QuestForm(ModelForm):
    class Meta:
        model = Quest
        exclude = ('activation_date', 'status',)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class QuestMixin(object):
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        # Here you can make any other adjustments to the model
        # ..
        self.object.save()
        print("test")
        self.inform_user()
        return super(QuestCreateView, self).form_valid(form)

    def inform_user(self):
        subject = "New quest from %s" % self.object.owner
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
