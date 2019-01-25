#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import ci_deploy_service_view


deploy_service_router=[url(r"deploy_service/(?P<id>.+)/$",ci_deploy_service_view.CIDeployServiceView.as_view()),
                       url(r"deploy_service_replace_config/(?P<id>.+)/$",ci_deploy_service_view.CIDeployServiceReplaceConfigView.as_view())
             ]
