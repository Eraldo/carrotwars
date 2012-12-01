from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from relations.models import Relation
from quests.models import Quest
from rewards.models import Reward
from django.db.models import Q

class MetaMixin:
    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()
    allowed_methods = ['get']

class UserResource(ModelResource):
    class Meta(MetaMixin):
        queryset = User.objects.all()
        fields = ['username']

class RelationResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')
    quester = fields.ForeignKey(UserResource, 'quester')

    class Meta(MetaMixin):
        queryset = Relation.objects.all()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(owner=request.user) | Q(quester=request.user))


class QuestResource(ModelResource):
    relation = fields.ForeignKey(RelationResource, 'relation')

    class Meta(MetaMixin):
        queryset = Quest.objects.all()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(relation__owner=request.user) | Q(relation__quester=request.user))

class RewardResource(ModelResource):
    relation = fields.ForeignKey(RelationResource, 'relation')

    class Meta(MetaMixin):
        queryset = Reward.objects.all()
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(relation__owner=request.user) | Q(relation__quester=request.user))


