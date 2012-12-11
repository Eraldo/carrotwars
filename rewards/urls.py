from django.conf.urls import patterns, url
from rewards.models import Reward
from rewards.views import RewardListView, RewardDetailView, RewardCreateView, RewardDeleteView, RewardUpdateView

urlpatterns = patterns('',
    # ex: /rewards/
    url(r'^$',
        RewardListView.as_view(),
        name='list'),
    # ex: /reward/4/
    url(r'^(?P<pk>\d+)/$',
        RewardDetailView.as_view(
            model=Reward,
            template_name='rewards/detail.html'),
        name='detail'),
    # ex: /rewards/add/
    url(r'^add$',
        RewardCreateView.as_view(
            model=Reward,
            ),
        name='add'),

)
