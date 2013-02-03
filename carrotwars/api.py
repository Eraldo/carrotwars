#!/usr/bin/env python
"""
This module contains the RESTful API settings.
This module can be used to get access to get json objects via resource URIs.
User permissions still apply.
"""

from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from relations.models import Relation
from quests.models import Quest
from rewards.models import Reward
from django.db.models import Q

__author__ = "Eraldo Helal"


class MetaMixin:
    """
    Mixin class to enable subclasses to inherit permission settings.
    """
    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()
    allowed_methods = ['get', 'put']


class UserResource(ModelResource):
    """
    An api model resource representung user objects.
    """
    class Meta(MetaMixin):
        queryset = User.objects.all()
        fields = ['username']


class RelationResource(ModelResource):
    """
    An api model resource representung user-relation objects.
    """
    owner = fields.ForeignKey(UserResource, 'owner')
    quester = fields.ForeignKey(UserResource, 'quester')

    class Meta(MetaMixin):
        queryset = Relation.objects.all()

    def apply_authorization_limits(self, request, object_list):
        """
        Limits api user-relation requests to allowed (owned or related) objects.
        (using django filters)
        """
        return object_list.filter(Q(owner=request.user) | Q(quester=request.user))


class QuestResource(ModelResource):
    """
    An api model resource representung quest objects.
    """
    relation = fields.ForeignKey(RelationResource, 'relation')

    class Meta(MetaMixin):
        queryset = Quest.objects.all()

    def apply_authorization_limits(self, request, object_list):
        """
        Limits api quest requests to allowed (owned or related) objects.
        (using django filters)
        """
        return object_list.filter(Q(relation__owner=request.user) | Q(relation__quester=request.user))

class RewardResource(ModelResource):
    """
    An api model resource representung reward objects.
    """
    relation = fields.ForeignKey(RelationResource, 'relation')

    class Meta(MetaMixin):
        queryset = Reward.objects.all()
    
    def apply_authorization_limits(self, request, object_list):
        """
        Limits api reward requests to allowed (owned or related) objects.
        (using django filters)
        """
        return object_list.filter(Q(relation__owner=request.user) | Q(relation__quester=request.user))


