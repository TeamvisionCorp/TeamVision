#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.home.views.home_autotask_view import index_list




autotask_router =[url(r"autotask/(all)",index_list),url(r"autotask/(ui)",index_list),url(r"autotask/(interface)",index_list),]
