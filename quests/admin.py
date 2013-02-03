#!/usr/bin/env python
"""
Contains the django admin interface settings related to the quest model.
"""

from django.contrib import admin
from quests.models import Quest

__author__ = "Eraldo Helal"


admin.site.register(Quest)
