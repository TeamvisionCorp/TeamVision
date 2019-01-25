#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views import project_task_view
from doraemon.project.views.project_task_view import index_list,edit,get_create_dialog,create,delete,update_property,more_tasks

task_router=[url(r"^(\d{1,6})/task/([a-zA-Z]*$)",index_list),
             url(r"^(\d{1,6})/task/([a-zA-Z]*)/get_more_task$",more_tasks),
             url(r"^(\d{1,6})/task/([a-zA-Z]*)/owner/(\d{1,9})",project_task_view.owner_tasks),
             url(r"^(\d{1,6})/task/(\d{1,6}$)",edit),
             url(r"^task/create_dialog$",get_create_dialog),
             url(r"^task/create",create),
             url(r"^task/(\d{1,6})/delete$",delete),
             url(r"^task/(\d{1,6})/update_property",update_property),
             ]