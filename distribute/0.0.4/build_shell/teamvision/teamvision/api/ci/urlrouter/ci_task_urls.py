#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views.ci_task_view import get_task,get_task_queue,tq_done,upload_package
from teamvision.api.ci.views import ci_task_history_view
from teamvision.api.ci.views import ci_task_parameter_view


api_task_router=[url(r"task/get_task$",get_task),
                 url(r"task/get_task_queue",get_task_queue),
                 url(r"task/tq_done",tq_done),
                 url(r"task/upload_package$",upload_package),
             ]

task_history_router=[url(r"task_history/(?P<id>.+)/$",ci_task_history_view.CITaskHistoryView.as_view()),
                         url(r"task/(?P<task_id>.+)/task_histories/$",ci_task_history_view.CITaskHistoryListView.as_view()),
                         url(r"task/parameter_group/(?P<id>.+)/$",ci_task_parameter_view.CITaskParameterGroupView.as_view()),
                         url(r"task/(?P<task_id>.+)/parameter_groups/$",ci_task_parameter_view.CITaskParameterGroupListView.as_view()),
                         url(r"task_history/(?P<history_id>.+)/clean_history$",ci_task_history_view.CITaskCleanHistoryView.as_view()),
                         url(r"task_history/(?P<history_id>.+)/change_log$",ci_task_history_view.CITaskHistoryChangeLogView.as_view()),
                         ]
