#!/usr/bin/env python
"""
Contains the UserProfile model and initial generation functionality.
"""

from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save

__author__ = "Eraldo Helal"


class UserProfile(models.Model):
    """
    A django model representing a persistant user profile bound to an existing user.
    On user creation via social login, avatar images get added to the related user profile.
    """

    # This field is required.
    user = models.OneToOneField(User)
    # Other fields here
    avatar = models.ImageField(upload_to='profiles/avatars', default='profiles/avatars/default.jpg', blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user

# post_save.connect(create_user_profile, sender=User)

# easy access to user profile: user.profile.field_name
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.google import GoogleOAuth2Backend
from social_auth.signals import socialauth_registered
def new_users_handler(sender, user, response, details, **kwargs):
    """
    Tries to get avatar images from social user login information on new user creation
    and generates profiles based on that information assoziated to that user.
    """
    user.is_new = True
    if user.is_new:
        if "id" in response:
            
            from urllib2 import urlopen, HTTPError
            from django.template.defaultfilters import slugify
            from django.core.files.base import ContentFile
            
            try:
                url = None
                if sender == FacebookBackend:
                    url = "http://graph.facebook.com/%s/picture?type=large" \
                        % response["id"]
                elif sender == GoogleOAuth2Backend and "picture" in response:
                    url = response["picture"]
                    
                if url:
                    avatar = urlopen(url)
                    profile = UserProfile(user=user)
                    
                    profile.avatar.save(slugify(user.username + " social") + '.jpg',
                                               ContentFile(avatar.read()))              
                    
                    profile.save()
                    
            except HTTPError:
                pass
                
    return False


socialauth_registered.connect(new_users_handler, sender=None)
