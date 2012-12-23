from rewards.models import Reward
from relations.models import Relation
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rewards.tables import OwnedRewardTable, AssignedRewardTable
from postman.api import pm_write
from django.core.urlresolvers import reverse
from django.contrib import messages

from rewards.tables import OwnedRewardTable, AssignedRewardTable

class RewardForm(ModelForm):
    quester = forms.ModelChoiceField(queryset = User.objects.all())

    def __init__(self, user=None, **kwargs):
        super(RewardForm, self).__init__(**kwargs)
        if user:
            self.fields['relation'].queryset = Relation.objects.filter(owner=user)

    class Meta:
        model = Reward
        exclude = ('relation', 'status',)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class RewardMixin(LoginRequiredMixin):
    model = Reward
    form_class = RewardForm
    
    def get_context_data(self, **kwargs):
        context = super(RewardMixin, self).get_context_data(**kwargs)
        context['owned'] = Reward.objects.owned_by(self.request.user)
        context['assigned'] = Reward.objects.assigned_to(self.request.user)
        context['owned_table'] = OwnedRewardTable(context['owned'])
        context['assigned_table'] = AssignedRewardTable(context['assigned'])
        return context

class RewardListView(RewardMixin, ListView):
    pass

class RewardDetailView(RewardMixin, DetailView):
    pass

class RewardCreateView(RewardMixin, CreateView):
    success_url = '.' # reverse('rewards:list')

    def get_form(self, form_class):
        form = super(RewardCreateView, self).get_form(form_class)
        owned_relations = Relation.objects.owned_by(self.request.user)
        form.fields['quester'].queryset = User.objects.filter(pk__in=owned_relations.values('quester'))
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.relation = Relation.objects.get(owner=self.request.user, quester=form.cleaned_data['quester'])
        self.object.save()
        self.inform_user()
        messages.add_message(self.request, messages.INFO, 'New reward has been created.')
        return super(RewardCreateView, self).form_valid(form)

    def inform_user(self):
        subject = "New reward!"
        body = """<a href="%s">%s</a>""" % (self.object.get_absolute_url(), self.object.title)
        pm_write(
            sender=self.request.user,
            recipient=self.object.relation.quester,
            subject=subject,
            body=body
            )


class RewardDeleteView(RewardMixin, DeleteView):
    pass


class RewardUpdateView(RewardMixin, UpdateView):
    pass


class BuyView(RedirectView):
    def get_redirect_url(self, pk):
            
        reward = Reward.objects.get(pk=pk)
        relation = Relation.objects.get(owner=reward.relation.owner, quester=self.request.user)

        if relation.balance < reward.price:
                messages.add_message(self.request, messages.ERROR, 'Not enough carrots. You have %s carrots from %s.' % (relation.balance, relation.owner))
                return reverse('rewards:list')

        # update reward
        reward.status = 'D'
        reward.save()

        # update balance
        relation = Relation.objects.get(owner=reward.relation.owner, quester=self.request.user)
        relation.balance -= reward.price
        relation.save()
        
        messages.add_message(self.request, messages.INFO, 'Reward has been bought. %s has been informed.' % reward.relation.owner)
        pm_write(
            sender=self.request.user,
            recipient=reward.relation.owner,
            subject="Reward %s has been bought." % reward.title,
            body=""
            )
        return reverse('rewards:list')
