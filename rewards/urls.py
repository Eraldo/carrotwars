from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from rewards.models import Reward
from rewards.views import RewardListView

urlpatterns = patterns('',
    # ex: /rewards/
    url(r'^$',
        RewardListView.as_view(),
        name='list'),
    # ex: /reward/4/
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Reward,
            template_name='rewards/detail.html'),
        name='detail'),
)
