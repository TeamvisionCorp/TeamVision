#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from doraemon.automationtesting.views.autorunresultview import create_add
from doraemon.automationtesting.views.autorunresultview import update_edit
from doraemon.automationtesting.views.autorunresultview import index_list
from doraemon.automationtesting.views.autorunresultview import get_list,init_autorunresult_formcontrol,get_autorunresult_page_counts
from doraemon.automationtesting.views.autorunresultview import copy_autorunresult,delete_autorunresult

urlpatterns = patterns(r"autorunresult",url(r"create",create_add),
                       url(r"edit",update_edit),
                       url(r"index",index_list),
                       url(r"getlist",get_list),
                       url(r"init_autorunresult_formcontrol",init_autorunresult_formcontrol),
                       url(r"get_autorunresult_page_counts",get_autorunresult_page_counts),
                       url(r"copyautorunresult",copy_autorunresult),
                       url(r"deleteautorunresult",delete_autorunresult)
                       )
