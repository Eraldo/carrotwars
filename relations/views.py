from django.views.generic import ListView
from relations.models import Relation

class RelationListView(ListView):
    context_object_name = 'all_relations'
    # template_name = 'quests/list.html'

    model = Relation
    
    def get_context_data(self, **kwargs):
        context = super(RelationListView, self).get_context_data(**kwargs)
        context['owned_relations'] = Relation.relations.get_owned_relations(self.request.user)
        context['assigned_relations'] = Relation.relations.get_assigned_relations(self.request.user)
        return context
