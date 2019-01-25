#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.ci.views.ci_deploy_view import index_list,config_task,task_history,task_parameter,build_with_parameter_page
from doraemon.ci.views import ci_deploy_view
from doraemon.ci.views.ci_task_view import start_task


deploy_router =[url(r"deploy/(all)",index_list),
                url(r"deploy/product/(\d{1,9})$",index_list),
                url(r"deploy/(\d{1,9})/(history)$",task_history),
                url(r"deploy/(\d{1,9})/(config)",config_task),
                url(r"deploy/(\d{1,9})/(parameter)$",task_parameter),
                url(r"deploy/(\d{1,9})/(build)$",build_with_parameter_page),
                url(r"deploy/(\d{1,9})/(changelog)$",ci_deploy_view.task_changelog),
                url(r"deploy/(\d{1,9})/start$",start_task),
                ]
