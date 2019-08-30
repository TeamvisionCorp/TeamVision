#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from teamvision.administrate.urlrouter.admin_user_urls import admin_user_router
from teamvision.administrate.urlrouter.admin_system_role_urls import admin_system_role_router
from teamvision.administrate.urlrouter.admin_permission_urls import admin_permission_router
from teamvision.administrate.urlrouter.admin_device_urls import admin_device_router
from teamvision.administrate.urlrouter.admin_project_urls import admin_project_router

urlpatterns =admin_user_router+admin_system_role_router+admin_permission_router+admin_device_router+admin_project_router