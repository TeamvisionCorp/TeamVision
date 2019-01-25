#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.project.views import project_version_view



api_version_router=[url(r"project_version/(?P<id>.+)/$",project_version_view.ProjectVersionView.as_view()),
                         url(r"project_versions/(?P<project_id>.+)/$",project_version_view.ProjectVersionListView.as_view()),
                         url(r"(?P<project_id>.+)/versions/$",project_version_view.ProjectVersionListView.as_view()),
                         ]

