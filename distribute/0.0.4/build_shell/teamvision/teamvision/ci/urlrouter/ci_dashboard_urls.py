#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.ci.views.ci_dashboard_view import index_list,get_build_log_dialog,add_message
from teamvision.ci.views import ci_dashboard_view,ci_task_view



dashboard_router =[url(r"task$",index_list),
                   url(r"dashboard/build_log_dialog$",get_build_log_dialog),
                   url(r'dashboard/add_message$',add_message),
                   url(r'dashboard/agent_list',ci_dashboard_view.get_agent_list),
                   url(r'dashboard/tq_list',ci_dashboard_view.get_task_queue_list),
                   url(r'dashboard/pre_build_log',ci_dashboard_view.pre_build_log),
                   url(r'dashboard/pre_build_log',ci_dashboard_view.pre_build_log),
                   url(r'dashboard/more_tasks',ci_task_view.more_dashboard_task_list),
                   ]
