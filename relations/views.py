from relations.models import Relation
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView
from django.views.generic.edit import ModelFormMixin
from django.forms import ModelForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from relations.tables import OwnedRelationTable, AssignedRelationTable, PendingRelationTable
from postman.api import pm_write
from django.core.urlresolvers import reverse
from django.contrib import messages

class RelationForm(ModelForm):
    
    class Meta:
        model = Relation
        fields = ('quester',)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class RelationMixin(LoginRequiredMixin):
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
    success_url = '.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.inform_user()
        messages.add_message(self.request, messages.INFO, 'New relation has been created. Waiting for Quester to accept.')
        return super(RelationCreateView, self).form_valid(form)

    def inform_user(self):
        subject = "New relation requested by %s" % self.object.owner
        body = """<a href="%s">%s</a>""" % (self.object.get_absolute_url(), self.object.owner)
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

class AcceptView(RedirectView):
    def get_redirect_url(self, pk):
        relation = Relation.objects.get(pk=pk)

        # check permission
        if self.request.user != relation.quester or relation.status != 'C':
            return reverse('relations:list')

        # update relation
        relation.status = 'A'
        relation.save()
        
        messages.add_message(self.request, messages.INFO, 'Relation has been accepted.')
        return reverse('relations:list')

class DeclineView(RedirectView):
    def get_redirect_url(self, pk):
        relation = Relation.objects.get(pk=pk)

        # check permission
        if self.request.user != relation.quester or relation.status != 'C':
            return reverse('relations:list')

        # update relation
        relation.status = 'R'
        relation.save()
        
        messages.add_message(self.request, messages.INFO, 'Relation has been declined.')
        return reverse('relations:list')
