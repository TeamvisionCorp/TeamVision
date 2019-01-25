# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.project.views import project_task_view

api_task_router = [url(r"task/(?P<task_id>.+)/$", project_task_view.PorjectTaskView.as_view()),
                   url(r"(?P<project_id>.+)/version/(?P<version_id>.+)/project_tasks$", project_task_view.ProjectTaskListView.as_view()),
                   ]
