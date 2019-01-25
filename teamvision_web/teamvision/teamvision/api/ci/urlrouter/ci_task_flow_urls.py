#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import ci_task_flow_view

ci_task_flow_router=[
                 url(r"task_flow/(?P<id>.+)/(?P<operation>.+)/$",ci_task_flow_view.CITaskFlowOperationView.as_view()),
                 url(r"task_flow/(?P<id>.+)/$",ci_task_flow_view.CITaskFlowView.as_view()),
                 url(r"task_flow/list",ci_task_flow_view.CITaskFlowListView.as_view()),
                 url(r"task_flow/my",ci_task_flow_view.CITaskFlowMyListView.as_view()),
                 url(r"task_flow/section/(?P<id>.+)",ci_task_flow_view.CITaskFlowSectionView.as_view()),
                 url(r"flow_section/(?P<id>.+)/(?P<operation>.+)/$",ci_task_flow_view.CIFlowSectionOperationView    .as_view()),
                 url(r"task_flow/(?P<flow_id>.+)/sections",ci_task_flow_view.CITaskFlowSectionListView.as_view()),
                 ]