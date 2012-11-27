from django.views.generic import ListView
from rewards.models import Reward

class RewardListView(ListView):
    context_object_name = 'all_rewards'
    template_name = 'rewards/list.html'

    model = Reward
    def get_context_data(self, **kwargs):
        context = super(RewardListView, self).get_context_data(**kwargs)
        context['owned_rewards'] = Reward.rewards.get_owned_rewards(self.request.user)
        context['offered_rewards'] = Reward.rewards.get_offered_rewards(self.request.user)
        return context
