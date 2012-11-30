from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from relations.models import Relation
from quests.models import Quest
from rewards.models import Reward

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class RelationResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')
    quester = fields.ForeignKey(UserResource, 'quester')

    class Meta:
        queryset = Relation.relations.all()

class QuestResource(ModelResource):
    relation = fields.ForeignKey(RelationResource, 'relation')

    class Meta:
        queryset = Quest.objects.all()

class RewardResource(ModelResource):
    relation = fields.ForeignKey(RelationResource, 'relation')

    class Meta:
        queryset = Reward.objects.all()
