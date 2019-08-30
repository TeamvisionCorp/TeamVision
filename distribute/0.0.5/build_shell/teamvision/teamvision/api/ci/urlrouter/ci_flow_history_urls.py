#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import ci_flow_history_view

ci_flow_history_router=[
                 url(r"task_flow/(?P<flow_id>.+)/history/list$",ci_flow_history_view.CITaskFlowHistoryListView.as_view()),
                 url(r"flow_history/(?P<id>.+)/$",ci_flow_history_view.CITaskFlowHistoryView.as_view()),
                 url(r"flow_history/(?P<flow_history_id>.+)/section_history/list",ci_flow_history_view.CIFlowSectionHistoryListView.as_view()),
                 url(r"section_history/(?P<id>.+)",ci_flow_history_view.CIFlowSectionHistoryView.as_view()),
                 ]