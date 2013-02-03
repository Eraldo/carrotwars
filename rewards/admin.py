#!/usr/bin/env python
"""
Contains the django admin interface settings related to the reward model.
"""

from django.contrib import admin
from rewards.models import Reward

__author__ = "Eraldo Helal"


admin.site.register(Reward)
