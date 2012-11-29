from django.views.generic import ListView
from quests.models import Quest

class QuestListView(ListView):
    context_object_name = 'all_quests'
    template_name = 'quests/list.html'

    model = Quest
    
    def get_context_data(self, **kwargs):
        context = super(QuestListView, self).get_context_data(**kwargs)
        context['owned_quests'] = Quest.quests.get_owned_quests(self.request.user)
        context['assigned_quests'] = Quest.quests.get_assigned_quests(self.request.user)
        return context
