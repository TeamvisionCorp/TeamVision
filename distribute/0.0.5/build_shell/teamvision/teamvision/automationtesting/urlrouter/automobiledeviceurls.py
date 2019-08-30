#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from teamvision.automationtesting.views.automobiledeviceview import create_add
from teamvision.automationtesting.views.automobiledeviceview import update_edit
from teamvision.automationtesting.views.automobiledeviceview import index_list
from teamvision.automationtesting.views.automobiledeviceview import get_list,init_automobiledevice_formcontrol,get_automobiledevice_page_counts
from teamvision.automationtesting.views.automobiledeviceview import copy_automobiledevice,delete_automobiledevice

urlpatterns = patterns(r"automobiledevice",url(r"create",create_add),
                       url(r"edit",update_edit),
                       url(r"index",index_list),
                       url(r"getlist",get_list),
                       url(r"init_automobiledevice_formcontrol",init_automobiledevice_formcontrol),
                       url(r"get_automobiledevice_page_counts",get_automobiledevice_page_counts),
                       url(r"copyautomobiledevice",copy_automobiledevice),
                       url(r"deleteautomobiledevice",delete_automobiledevice)
                       )
