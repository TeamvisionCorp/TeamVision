#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from doraemon.toolbox.views.toolboxview import index_list
from doraemon.toolbox.views.commonview import loadleftnavigater
from doraemon.toolbox.views.toolboxview import get_toolpage




urlpatterns = patterns(
                       r"toolbox",url(r"index",index_list),
                       url(r"getleftnavigater",loadleftnavigater),
                       url(r"gettoolpage",get_toolpage),
                       )
