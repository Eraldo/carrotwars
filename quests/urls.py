from django.conf.urls import patterns, url
from quests.models import Quest
from quests.views import QuestListView, QuestDetailView, QuestCreateView, QuestDeleteView, QuestUpdateView, AcceptView, DeclineView, CompleteView, ConfirmView, DenyView

urlpatterns = patterns('',
    # ex: /quests/
    url(r'^$',
        QuestListView.as_view(),
        name='list'),
    # ex: /quests/4/
    url(r'^(?P<pk>\d+)/$',
        QuestDetailView.as_view(),
        name='detail'),
    # ex: /quests/add/
    url(r'^add$',
        QuestCreateView.as_view(),
        name='add'),
    # ex: /quests/4/accept/
    url(r'^(?P<pk>\d+)/accept/$',
        AcceptView.as_view(),
        name='accept'),
    # ex: /quests/4/decline/
    url(r'^(?P<pk>\d+)/decline/$',
        DeclineView.as_view(),
        name='decline'),
    # ex: /quests/4/complete/
    url(r'^(?P<pk>\d+)/complete/$',
        CompleteView.as_view(),
        name='complete'),
    # ex: /quests/4/confirm/
    url(r'^(?P<pk>\d+)/confirm/$',
        ConfirmView.as_view(),
        name='confirm'),
    # ex: /quests/4/deny/
    url(r'^(?P<pk>\d+)/deny/$',
        DenyView.as_view(),
        name='deny'),
)
