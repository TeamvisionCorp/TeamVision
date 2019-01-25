#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.ci.views import ci_task_plugin_view


task_plugin_router=[url(r"task_plugin/(?P<id>.+)/$",ci_task_plugin_view.CITaskPluginView.as_view()),
                         url(r"task_plugins$",ci_task_plugin_view.CITaskPluginListView.as_view()),]