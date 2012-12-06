from django.conf.urls import patterns, url
from django.views.generic import DetailView, UpdateView, FormView, CreateView
from quests.models import Quest
from quests.views import QuestListView, QuestDetailView, QuestCreateView, QuestDeleteView, QuestUpdateView, AcceptView, DeclineView

urlpatterns = patterns('',
    # ex: /quests/
    url(r'^$',
        QuestListView.as_view(),
        name='list'),
    # ex: /quests/4/
    url(r'^(?P<pk>\d+)/$',
        QuestUpdateView.as_view(
            model=Quest,
            ),
        name='detail'),
    # ex: /quests/add/
    url(r'^add$',
        QuestCreateView.as_view(
            model=Quest,
            ),
        name='add'),
    # ex: /quests/4/accept/
    url(r'^(?P<pk>\d+)/accept/$',
        AcceptView.as_view(),
        name='accept'),
    # ex: /quests/4/decline/
    url(r'^(?P<pk>\d+)/decline/$',
        DeclineView.as_view(),
        name='decline'),
)
