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
from teamvision.automationtesting.views.automationtaskview import get_list
from teamvision.automationtesting.views.commonview import loadleftnavigater
from teamvision.automationtesting.views.automationtaskview import get_mylist

urlpatterns = patterns(r"automationtask/automationtask",url(r"create",create_add),url(r"edit",update_edit)
                       ,url(r"index",index_list),url(r"gettasklist",get_list),
                       url(r"getleftnavigater",loadleftnavigater),
                       url(r"getmytasklist",get_mylist)
                       )
