#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.ci.views import ci_crendentials_view


ci_crendentials_router=[url(r"crendential/(?P<id>.+)/$",ci_crendentials_view.CICrendentialsView.as_view()),
                         url(r"crendentials$",ci_crendentials_view.CICrendentialsListView.as_view()),]