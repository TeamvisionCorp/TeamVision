#coding=utf-8
from django.conf.urls import  url,include
from rest_framework.documentation import include_docs_urls




urlpatterns = [
    url(r'^docs/', include_docs_urls(title='Teamvision API')),
    url(r'project/', include('teamvision.api.project.urlrouter.project_urls')),
    url(r'ucenter/', include('teamvision.api.ucenter.urlrouter.ucenter_urls')),
    url(r'home/', include('teamvision.api.home.urlrouter.home_urls')),
    url(r'logcat/', include('teamvision.api.logcat.urlrouter.logcat_urls')),
    url(r'ci/', include('teamvision.api.ci.urlrouter.ci_urls')),
    url(r'interface/', include('teamvision.api.interface.urlrouter.interface_urls')),
    url(r'auth/', include('teamvision.api.auth.urlrouter.auth_urls')),
    url(r'common/', include('teamvision.api.common.urlrouter.common_urls')),
    ]