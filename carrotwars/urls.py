from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from ajax_select import urls as ajax_select_urls

# api
from tastypie.api import Api
from carrotwars.api import UserResource, RelationResource, QuestResource, RewardResource

admin.autodiscover()

# api config
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RelationResource())
v1_api.register(QuestResource())
v1_api.register(RewardResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carrotwars.views.home', name='home'),
    # url(r'^carrotwars/', include('carrotwars.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # login page
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    # logout page
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    # main urls
    url(r'^$', lambda x: redirect('/quests'), name='home'),
    url(r'^relations/', include('relations.urls', namespace="relations")),
    url(r'^quests/', include('quests.urls', namespace="quests")),
    url(r'^rewards/', include('rewards.urls', namespace="rewards")),
    url(r'^messages/', include('postman.urls')),

    # include the lookup urls
    url(r'^admin/lookups/', include(ajax_select_urls)),
    # include the admin interface
    url(r'^admin/', include(admin.site.urls)),

    # include api
    url(r'^api/', include(v1_api.urls)),
)

from django.conf import settings

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
