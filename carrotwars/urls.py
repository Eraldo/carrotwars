from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carrotwars.views.home', name='home'),
    # url(r'^carrotwars/', include('carrotwars.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', lambda x: redirect('/quests')),
    url(r'^relations/', include('relations.urls', namespace="relations")),
    url(r'^quests/', include('quests.urls', namespace="quests")),
    url(r'^rewards/', include('rewards.urls', namespace="rewards")),
    url(r'^messages/', include('postman.urls')),

    # include the lookup urls
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
