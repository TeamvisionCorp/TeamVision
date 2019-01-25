#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.ci.views import ci_deploy_server_view


deploy_server_router=[url(r"deploy_server/(?P<id>.+)/$",ci_deploy_server_view.CIDeployServerView.as_view()),
#                          url(r"deploy_servers$",ci_deploy_server_view.CIDeployServerListView.as_view()),
                         url(r"deploy_servers/$",ci_deploy_server_view.CIDeployServerListView.as_view()),]
