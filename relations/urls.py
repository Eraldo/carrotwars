from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView, UpdateView, FormView, CreateView
from relations.models import Relation
from relations.views import RelationListView, RelationDetailView, RelationCreateView, RelationDeleteView, RelationUpdateView

urlpatterns = patterns('',
    # ex: /relations/
    url(r'^$',
        RelationListView.as_view(),
        name='list'),
    # ex: /relations/4/
    url(r'^(?P<pk>\d+)/$',
        RelationDetailView.as_view(),
        name='detail'),
    # ex: /relations/add/
    url(r'^add$',
        RelationCreateView.as_view(),
        name='add'),
)
