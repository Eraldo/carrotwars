from django.views.generic import ListView
from quests.models import Quest

class QuestListView(ListView):
    model = Quest
    
    def get_context_data(self, **kwargs):
        context = super(QuestListView, self).get_context_data(**kwargs)
        context['owned'] = Quest.objects.owned_by(self.request.user)
        context['assigned'] = Quest.objects.assigned_to(self.request.user)
        return context
