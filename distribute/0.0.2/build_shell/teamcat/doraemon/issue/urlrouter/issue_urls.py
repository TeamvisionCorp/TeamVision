#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from doraemon.interface.urlrouter.env_portal_urls import portal_router
from doraemon.interface.urlrouter.env_dashboard_urls import dashboard_router

urlpatterns =portal_router+dashboard_router