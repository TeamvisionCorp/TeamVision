#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from teamvision.automationtesting.views.automationtaskview import create_add
from teamvision.automationtesting.views.automationtaskview import update_edit
from teamvision.automationtesting.views.automationtaskview import index_list
from teamvision.automationtesting.views.automationtaskview import get_list,init_autotask_formcontrol,get_autotask_page_counts,get_autotask_namelist
from teamvision.automationtesting.views.automationtaskview import copy_autotask,delete_autotask,check_name_exits,start_task,stop_task

urlpatterns = patterns(r"autotask",url(r"create",create_add),
                       url(r"edit",update_edit),
                       url(r"index",index_list),
                       url(r"getlist",get_list),
                       url(r"init_autotask_formcontrol",init_autotask_formcontrol),
                       url(r"get_autotask_page_counts",get_autotask_page_counts),
                       url(r"copyautotask",copy_autotask),
                       url(r"deleteautotask",delete_autotask),
                       url(r"get_taskname_list",get_autotask_namelist),
                       url(r"check_name_exits",check_name_exits),
                       url(r"starttask",start_task),
                       url(r"stoptask",stop_task),
                       )
