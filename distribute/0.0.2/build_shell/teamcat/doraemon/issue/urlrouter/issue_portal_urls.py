#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.interface.views.portal_view import all,env_filter

portal_router=[url(r"portal/all$",all),
               url(r"portal/filter$",env_filter),]