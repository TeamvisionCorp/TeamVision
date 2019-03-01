#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.ci.views import ci_task_parameter_view
from teamvision.ci.views.ci_task_parameter_view import edit,create,save,delete,copy
from teamvision.ci.views.ci_task_parameter_view import get_task_parameter_group_list,task_parameter_keyvalue_controll

task_parameter_router =[
              url(r"task/parameter_group/edit$",edit),
              url(r"task/(\d{1,9})/parameter_group/create$",create),
              url(r"task/(\d{1,9})/parameter_group/list$",get_task_parameter_group_list),
              url(r"task/parameter/keyvalue_controll",task_parameter_keyvalue_controll),
              url(r"task/parameter_group/save$",save),
              url(r"task/parameter_group/delete$",delete),
              url(r"task/parameter_group/copy$",copy),
              url(r"task/parameter_group/confirm_dialog$",ci_task_parameter_view.confirm_dialog),
                ]
