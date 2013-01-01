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
from django_tables2 import RequestConfig

from rewards.tables import OwnedRewardTable, AssignedRewardTable

__author__ = "Eraldo Helal"

class RewardForm(ModelForm):
    quester = forms.ModelChoiceField(queryset = User.objects.all())

    class Meta:
        model = Reward
        exclude = ('relation', 'status',)

    def __init__(self, user=None, **kwargs):
        super(RewardForm, self).__init__(**kwargs)
        if user:
            self.fields['relation'].queryset = Relation.objects.filter(owner=user)

    # Add some custom validation to our image field
    def clean_image(self):
        max_size = 1 # in MB
        max_width = 600
        max_height = 600
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > max_size*1024*1024:
                raise forms.ValidationError("Image file is too large. (> %s MB)" % max_size)
            from PIL import Image
            img = Image.open(image)
            width, height = img.size
            if width > max_width or height > max_height:
                raise forms.ValidationError("Image file is too large. (> %s x %s)" % (max_width, max_height))
                # # TODO resize image (then update size [and type if it was not jpg] on the memory image file)
                # print("before:", image.file, image.field_name, image.name, image.content_type, image.size)
                # img.thumbnail((max_width, max_height), Image.ANTIALIAS)
                # img.save(image.file, "JPEG")
                # print("after:", image.file, image.field_name, image.name, image.content_type, image.size)
                # raise forms.ValidationError("Image file is too large. (> %s x %s)" % (max_width, max_height))
            return image
        else:
            raise forms.ValidationError("Couldn't read uploaded image")

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class RewardMixin(LoginRequiredMixin):
    model = Reward
    form_class = RewardForm
    
    def get_context_data(self, **kwargs):
        context = super(RewardMixin, self).get_context_data(**kwargs)
        context['owner'] = Relation.objects.owned_by(self.request.user)
        context['owned'] = Reward.objects.owned_by(self.request.user)
        context['assigned'] = Reward.objects.assigned_to(self.request.user)
        context['owned_table'] = OwnedRewardTable(context['owned'])
        context['assigned_table'] = AssignedRewardTable(context['assigned'])
        requestConfig = RequestConfig(self.request, paginate={"per_page": 10,})
        requestConfig.configure(context['owned_table'])
        requestConfig.configure(context['assigned_table'])
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

        # check if price is in range (between price_min and price_max)
        price_min = 1
        price_max = 100
        if price_min <= form.cleaned_data['price'] <= price_max: # in range ?
            pass # in range :)
        else: # out of range :|
            from django.forms.util import ErrorList
            errors = form._errors.setdefault("price", ErrorList())
            errors.append("The price needs to be between %s and %s." % (price_min, price_max))
            return self.render_to_response(self.get_context_data(form=form))
        
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

        # check permission
        if self.request.user != reward.relation.quester or reward.status != 'A':
            return reverse('quests:list')

        # check credits
        if relation.balance < reward.price:
            diff = reward.price - relation.balance
            messages.add_message(self.request, messages.ERROR, 'Not enough carrots. You have %s carrot%s from %s. You need %s more carrot%s.' % (relation.balance, "s"[relation.balance==1:], relation.owner, diff, "s"[diff==1:]))
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
