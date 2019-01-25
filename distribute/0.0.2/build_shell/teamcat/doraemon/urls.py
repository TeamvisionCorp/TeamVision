#coding=utf-8
from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.views import login,logout
from doraemon.home.views.home_page_view import home_page
admin.autodiscover()



urlpatterns =[

    url(r'^$',home_page),
    url(r'^ucenter/', include('doraemon.user_center.urlrouter.ucenter_urls')),
    url(r'^administrate/', include('doraemon.administrate.urlrouter.admin_urls')),
    url(r'^project/', include('doraemon.project.urlrouter.project_urls')),
    url(r'^home/', include('doraemon.home.urlrouter.home_urls')),
    url(r'^device/', include('doraemon.device.urlrouter.device_urls')),
    url(r'^logcat/', include('doraemon.logcat.urlrouter.logcat_urls')),
    # url(r'^env/', include('doraemon.env.urlrouter.env_urls')),
    url(r'^api/', include('doraemon.api.apiurls')),
    url(r'^ci/', include('doraemon.ci.urlrouter.ci_urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('doraemon.auth_extend.user.urlrouter.user_urls')),
    url(r'^accounts/login/$', login,{'template_name':'registration/userlogin.html'}),
    url(r'^accounts/logout/$', logout,{'template_name':'registration/userlogin.html',"next_page":"/"}),
    ]
