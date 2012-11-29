from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView, UpdateView, FormView
from relations.models import Relation
from relations.views import RelationListView

urlpatterns = patterns('',
    # ex: /relations/
    url(r'^$',
        RelationListView.as_view(
            model=Relation),
        name='list'),
    # ex: /relations/4/
    url(r'^(?P<pk>\d+)/$',
        UpdateView.as_view(
            model=Relation,
            ),
        name='detail'),
)
