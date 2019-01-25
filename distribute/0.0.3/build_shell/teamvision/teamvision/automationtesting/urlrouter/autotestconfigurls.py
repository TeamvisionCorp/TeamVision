#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from teamvision.automationtesting.views.autotestconfigview import create_add
from teamvision.automationtesting.views.autotestconfigview import update_edit
from teamvision.automationtesting.views.autotestconfigview import index_list
from teamvision.automationtesting.views.autotestconfigview import get_list,check_name_exits,init_autotestconfig_formcontrol,get_autotestconfig_page_counts
from teamvision.automationtesting.views.autotestconfigview import copy_autotestconfig,delete_autotestconfig

urlpatterns = patterns(r"autotestconfig",url(r"create",create_add),
                       url(r"edit",update_edit),
                       url(r"index",index_list),
                       url(r"getlist",get_list),
                       url(r"check_name_exits",check_name_exits),
                       url(r"init_autotestconfig_formcontrol",init_autotestconfig_formcontrol),
                       url(r"get_autotestconfig_page_counts",get_autotestconfig_page_counts),
                       url(r"copyautotestconfig",copy_autotestconfig),
                       url(r"deleteautotestconfig",delete_autotestconfig)
                       )
