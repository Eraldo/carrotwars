from quests.models import Quest
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quests.tables import OwnedQuestTable, AssignedQuestTable, PendingQuestTable

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

    # def form_valid(self, form):
    #     # save but don't commit the model form
    #     self.object = form.save(commit=False)
    #     # set the owner to be the current user
    #     # self.object.owner = self.request.user
    #     #
    #     # Here you can make any other adjustments to the model
    #     #
    #     self.object.save()
    #     # ok now call the base class and we are done.
    #     return super(ModelFormMixin, self).form_valid(form)


class QuestListView(QuestMixin, ListView):
    pass

class QuestDetailView(QuestMixin, DetailView):
    pass

class QuestCreateView(QuestMixin, CreateView):
    pass

class QuestDeleteView(QuestMixin, DeleteView):
    pass

class QuestUpdateView(QuestMixin, UpdateView):
    pass
