#!/usr/bin/env python
"""
Contains the reward related url mappings.
"""

from django.conf.urls import patterns, url
from rewards.models import Reward
from rewards.views import RewardListView, RewardDetailView, RewardCreateView, RewardDeleteView, RewardUpdateView, BuyView

__author__ = "Eraldo Helal"


urlpatterns = patterns('',
    # ex: /rewards/
    url(r'^$',
        RewardListView.as_view(),
        name='list'),
    # ex: /reward/4/
    url(r'^(?P<pk>\d+)/$',
        RewardDetailView.as_view(),
        name='detail'),
    # ex: /rewards/add/
    url(r'^add$',
        RewardCreateView.as_view(),
        name='add'),
    # ex: /rewards/4/buy/
    url(r'^(?P<pk>\d+)/buy/$',
        BuyView.as_view(),
        name='buy'),
)
