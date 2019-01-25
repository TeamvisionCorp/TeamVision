#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from doraemon.administrate.views import admin_system_role_view 

admin_system_role_router=[
                    url(r"systemrole/(all)$",admin_system_role_view.system_role),
                    url(r"systemrole/create$",admin_system_role_view.role_create),
                    url(r"systemrole/check_value_exists$",admin_system_role_view.check_value_exists),
                    url(r"systemrole/usergroup_list$",admin_system_role_view.userrole_list),
                    url(r"systemrole/(\d{1,6})/delete$",admin_system_role_view.role_delete),
                    url(r"systemrole/(\d{1,6})/edit_get$",admin_system_role_view.role_edit_get),
                    url(r"systemrole/(\d{1,6})/update_permission$",admin_system_role_view.update_role_permission),
                    url(r"systemrole/(\d{1,6})/group_permission_list$",admin_system_role_view.role_permission_list),
                    url(r"systemrole/(\d{1,6})/update_description",admin_system_role_view.update_description),
                 ]