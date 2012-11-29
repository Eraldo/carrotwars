from django.conf.urls import patterns, url
from django.views.generic import DetailView, UpdateView, FormView, CreateView
from quests.models import Quest
from quests.views import QuestListView

urlpatterns = patterns('',
    # ex: /quests/
    url(r'^$',
        QuestListView.as_view(),
        name='list'),
    # ex: /quests/4/
    url(r'^(?P<pk>\d+)/$',
        # DetailView.as_view(
        #     model=Quest,
        #     template_name='quests/detail.html'),
        # name='detail'),
        UpdateView.as_view(
            model=Quest,
            ),
        name='detail'),
    # ex: /quests/add/
    url(r'^add$',
        CreateView.as_view(
            model=Quest,
            ),
        name='add'),
)
