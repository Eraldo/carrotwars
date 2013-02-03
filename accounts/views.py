#!/usr/bin/env python
"""
Contains the reward model and a reward manager.
"""

from django.views.generic import RedirectView
from django.contrib import messages
from django.core.urlresolvers import reverse

__author__ = "Eraldo Helal"


class LoginErrorView(RedirectView):
    """
    A generic view that notifies the user on a failed long attempt
    and redirects back to the login page."""
    def get_redirect_url(self):        
        messages.add_message(self.request, messages.ERROR, 'Login failed.')
        return reverse('login')
