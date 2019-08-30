#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.ci.views.ci_task_view import create_dialog,task_config_basic,save_task_config,stop_task,download_package
from teamvision.ci.views.ci_task_view import create,update_property,get_task_config,copy,get_task_list,delete_task,start_task
from teamvision.ci.views import ci_task_view,ci_task_history_view

task_router =[url(r"task/create_dialog$",create_dialog),
              url(r"task/confirm_dialog$",ci_task_view.confirm_dialog),
              url(r"task/create$",create),
              url(r"task/copy/(\d{1,9})$",copy),
              url(r"task/delete/(\d{1,9})$",delete_task),
              url(r"task/clean_history/(\d{1,9})$",ci_task_view.clean_task_history),
              url(r"task/(\d{1,9})/start$",start_task),
              url(r"task/stop/(\d{1,9})$",stop_task),
              url(r"task/(\d{1,9})/update_property$",update_property),
              url(r"task/(\d{1,9})/task_config_basic$",task_config_basic),
              url(r"task/(\d{1,9})/config/save_task_config$",save_task_config),
              url(r"task/(\d{1,9})/config/get_task_config$",get_task_config),
              url(r"task/get_task_list$",get_task_list),
              url(r"task/search_task",ci_task_view.search_task),
              url(r"task/copytask",ci_task_view.copy_task),
                ]
