#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from teamvision.automationtesting.views.autoagentview import create_add
from teamvision.automationtesting.views.autoagentview import update_edit
from teamvision.automationtesting.views.autoagentview import index_list
from teamvision.automationtesting.views.autoagentview import get_list,check_name_exits,init_autoagent_formcontrol,get_autoagent_page_counts,check_ip_exits
from teamvision.automationtesting.views.autoagentview import copy_autoagent,delete_autoagent

urlpatterns = patterns(r"autoagent",url(r"create",create_add),
                       url(r"edit",update_edit),
                       url(r"index",index_list),
                       url(r"getlist",get_list),
                       url(r"check_name_exits",check_name_exits),
                       url(r"check_ip_exits",check_ip_exits),
                       url(r"init_autoagent_formcontrol",init_autoagent_formcontrol),
                       url(r"get_autoagent_page_counts",get_autoagent_page_counts),
                       url(r"copyautoagent",copy_autoagent),
                       url(r"deleteautoagent",delete_autoagent)
                       )
