#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.project.views import project_module_view



api_module_router=[url(r"project_module/(?P<id>.+)/$",project_module_view.PorjectModuleView.as_view()),
                         url(r"(?P<project_id>.+)/modules$",project_module_view.ProjectModuleListView.as_view()),
                         ]

