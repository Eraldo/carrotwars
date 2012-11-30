from relations.models import Relation
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.forms import ModelForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class RelationForm(ModelForm):
    class Meta:
        model = Relation
        exclude = ('owner', 'balance', 'status')

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class RelationMixin(LoginRequiredMixin):
    model = Relation
    form_class = RelationForm
    
    def get_success_url(self):
        return reverse('list')
    
    def get_context_data(self, **kwargs):
        context = super(RelationMixin, self).get_context_data(**kwargs)
        context['owned'] = Relation.objects.owned_by(self.request.user)
        context['assigned'] = Relation.objects.assigned_to(self.request.user)
        return context

    def form_valid(self, form):
        # save but don't commit the model form
        self.object = form.save(commit=False)
        # set the owner to be the current user
        self.object.owner = self.request.user
        #
        # Here you can make any other adjustments to the model
        #
        self.object.save()
        # ok now call the base class and we are done.
        return super(ModelFormMixin, self).form_valid(form)

class RelationListView(RelationMixin, ListView):
    pass

class RelationDetailView(RelationMixin, DetailView):
    pass

class RelationCreateView(RelationMixin, CreateView):
    pass

class RelationDeleteView(RelationMixin, DeleteView):
    pass

class RelationUpdateView(RelationMixin, UpdateView):
    pass
