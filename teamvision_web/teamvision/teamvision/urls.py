#coding=utf-8
from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.views import login,logout
from teamvision.home.views.home_page_view import home_page
admin.autodiscover()



urlpatterns =[

    url(r'^$',home_page),
    url(r'^ucenter/', include('teamvision.user_center.urlrouter.ucenter_urls')),
    url(r'^administrate/', include('teamvision.administrate.urlrouter.admin_urls')),
    url(r'^project/', include('teamvision.project.urlrouter.project_urls')),
    url(r'^home/', include('teamvision.home.urlrouter.home_urls')),
    url(r'^device/', include('teamvision.device.urlrouter.device_urls')),
    url(r'^logcat/', include('teamvision.logcat.urlrouter.logcat_urls')),
    # url(r'^env/', include('teamvision.env.urlrouter.env_urls')),
    url(r'^api/', include('teamvision.api.apiurls')),
    url(r'^ci/', include('teamvision.ci.urlrouter.ci_urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('teamvision.auth_extend.user.urlrouter.user_urls')),
    url(r'^accounts/login/$', login,{'template_name':'registration/userlogin.html'}),
    url(r'^accounts/logout/$', logout,{'template_name':'registration/userlogin.html',"next_page":"/"}),
    ]
