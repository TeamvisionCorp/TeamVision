#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.common.views import task_queue_view


api_task_queue_router =[url(r"task_queue/(?P<id>.+)",task_queue_view.TaskQueueView.as_view()),
                  url(r"task_queues$",task_queue_view.TaskQueueListView.as_view()),
                  ]
