# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.project.views import project_task_view

api_task_router = [url(r"task/(?P<task_id>\d{1,6})/$", project_task_view.PorjectTaskView.as_view()),
                   url(r"task/create/$", project_task_view.ProjectTaskListView.as_view()),
                   url(r"task/update/$", project_task_view.PorjectTaskView.as_view()),
                   url(r"task/delete/$", project_task_view.PorjectTaskView.as_view()),
                   url(r"(?P<project_id>.+)/version/(?P<version_id>.+)/project_tasks$", project_task_view.ProjectTaskListView.as_view()),
                   url(r"task/(?P<task_id>\d{1,6})/task_owners", project_task_view.ProjectTaskOwnerListView.as_view()),
                   url(r"task_owner/(?P<id>\d{1,6})/$", project_task_view.PorjectTaskOwnerView.as_view()),
                   url(r"task_owner/create/$", project_task_view.ProjectTaskOwnerListView.as_view()),
                   url(r"task_owner/update/$", project_task_view.PorjectTaskOwnerView.as_view()),
                   url(r"task_owner/delete/$", project_task_view.PorjectTaskOwnerView.as_view()),
                   url(r"task/task_owners", project_task_view.ProjectTaskOwnerListView.as_view()),
                   url(r"task_dependency/create/$", project_task_view.ProjectTaskDependencyListView.as_view()),
                   url(r"task_dependency/update/$", project_task_view.PorjectTaskDependencyView.as_view()),
                   url(r"task_dependency/delete/$", project_task_view.PorjectTaskDependencyView.as_view()),
                   url(r"task_dependencies", project_task_view.ProjectTaskDependencyListView.as_view()),
                   ]
