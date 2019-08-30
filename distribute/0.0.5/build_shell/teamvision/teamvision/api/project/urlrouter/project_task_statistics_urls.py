#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.project.views import task_statistics_view



api_task_statistics_router=[url(r"(?P<project_id>.+)/version/(?P<version_id>.+)/statistics/task_status_pie$",task_statistics_view.TaskStatusPie.as_view()),
url(r"(?P<project_id>.+)/version/(?P<version_id>.+)/statistics/task_summary_count$",task_statistics_view.TaskSummaryCount.as_view()),
                         ]

