from relations.models import Relation
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.forms import ModelForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from relations.tables import OwnedRelationTable, AssignedRelationTable, PendingRelationTable
from postman.api import pm_write

class RelationForm(ModelForm):
    class Meta:
        model = Relation
        fields = ('quester',)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class RelationMixin(object):
    model = Relation
    form_class = RelationForm
    
    def get_context_data(self, **kwargs):
        context = super(RelationMixin, self).get_context_data(**kwargs)
        context['owned'] = Relation.objects.owned_by(self.request.user)
        context['assigned'] = Relation.objects.assigned_to(self.request.user)
        context['pending'] = Relation.objects.pending_for(self.request.user)
        context['owned_table'] = OwnedRelationTable(context['owned'])
        context['assigned_table'] = AssignedRelationTable(context['assigned'])
        context['pending_table'] = PendingRelationTable(context['pending'])
        return context

class RelationListView(RelationMixin, ListView):
    pass

class RelationDetailView(RelationMixin, DetailView):
    pass

class RelationCreateView(RelationMixin, CreateView):

    def form_valid(self, form):
        # save but don't commit the model form
        self.object = form.save(commit=False)
        # set the owner to be the current user
        self.object.owner = self.request.user
        #
        # Here you can make any other adjustments to the model
        #
        self.object.save()
        self.inform_user()
        # ok now call the base class and we are done.
        return super(ModelFormMixin, self).form_valid(form)

    def inform_user(self):
        subject = "New relation requested by: %s" % self.object.owner
        body = "This is a test.\nWith 2 lines."
        pm_write(
            sender=self.request.user,
            recipient=self.object.quester,
            subject=subject,
            body=body
            )

class RelationDeleteView(RelationMixin, DeleteView):
    pass

class RelationUpdateView(RelationMixin, UpdateView):
    pass
