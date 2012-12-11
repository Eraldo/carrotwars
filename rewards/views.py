from rewards.models import Reward
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rewards.tables import OwnedRewardTable, AssignedRewardTable
from postman.api import pm_write
from django.core.urlresolvers import reverse

from rewards.tables import OwnedRewardTable, AssignedRewardTable

class RewardForm(ModelForm):
    class Meta:
        model = Reward
        exclude = ('status',)

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.inform_user()
        print(reverse('rewards:list'))
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
