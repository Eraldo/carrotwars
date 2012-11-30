from django.views.generic import ListView
from rewards.models import Reward

class RewardListView(ListView):
    model = Reward
    
    def get_context_data(self, **kwargs):
        context = super(RewardListView, self).get_context_data(**kwargs)
        context['owned'] = Reward.objects.owned_by(self.request.user)
        context['assigned'] = Reward.objects.assigned_to(self.request.user)
        return context
