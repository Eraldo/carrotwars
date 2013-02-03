#!/usr/bin/env python
"""
Contains the django admin interface settings related to the UserProfile model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User
from models import UserProfile

__author__ = "Eraldo Helal"


class ProfileInline(admin.StackedInline):
    """Meta information model to display user profiles inline."""
    model = UserProfile
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    """
    Meta information model to display Users
    with associated inline profile.
    """
    inlines = [ProfileInline,]


# refresh the admin user model settings
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
