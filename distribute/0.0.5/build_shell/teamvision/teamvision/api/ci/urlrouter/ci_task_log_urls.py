#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import ci_task_log_view

ci_task_log_router=[url(r"task/prelog/(?P<tq_id>.+)/$",ci_task_log_view.CITaskLogView.as_view()),
                 ]