#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.home.views.home_task_view import all,more_tasks,owner_tasks

task_router=[url(r"task/([a-zA-Z]*)$",all),
             url(r"task/([a-zA-Z]*)/get_more_task$",more_tasks),
             url(r"task/([a-zA-Z]*)/owner/(\d{1,9})",owner_tasks)
             ]