#coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'doraemon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^testcase/', include('doraemon.testcase.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG: 
    urlpatterns += patterns('', 
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH, 'show_indexes':True}), 
            )
