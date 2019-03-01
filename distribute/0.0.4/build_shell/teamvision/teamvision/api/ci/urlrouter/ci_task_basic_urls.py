#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import ci_task_basic_view

ci_task_basic_router=[url(r"task_basic/(?P<id>.+)/(?P<operation>.+)/$",ci_task_basic_view.CITaskOperationView.as_view()),
                 url(r"task_basic/(?P<id>.+)/$",ci_task_basic_view.CITaskBasicView.as_view()),
                 url(r"task_basic/list",ci_task_basic_view.CITaskBasicListView.as_view()),
                 url(r"task_basic/my",ci_task_basic_view.CITaskMyListView.as_view()),
                 url(r"project/my",ci_task_basic_view.CIMyProjectView.as_view()),
                 ]