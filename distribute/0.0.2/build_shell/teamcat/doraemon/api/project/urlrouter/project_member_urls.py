#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.project.views import project_memeber_view



api_member_router=[url(r"project_member/(?P<id>.+)/$",project_memeber_view.PorjectMemberView.as_view()),
                         url(r"project_members/(?P<project_id>.+)/$",project_memeber_view.ProjectMemberListView.as_view()),
                         url(r"(?P<project_id>.+)/project_members$",project_memeber_view.ProjectMemberListView.as_view()),
                         url(r"list$",project_memeber_view.ProjectListView.as_view()),
                         url(r"list/(?P<my>.+)$",project_memeber_view.ProjectListView.as_view()),
                         url(r"(?P<id>.+)/detail$",project_memeber_view.ProjectView.as_view()),
                         url(r"products$",project_memeber_view.ProductListView.as_view()),
                         ]

