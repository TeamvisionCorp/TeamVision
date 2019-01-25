#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from doraemon.administrate.views.admin_permission_view import permission,permission_create_dialog,permission_create,update_name,update_desc
from doraemon.administrate.views.admin_permission_view import check_value_exists,permission_delete

admin_permission_router=[
                    url(r"permission/(all)$",permission),
                    url(r"permission/create_dialog$",permission_create_dialog),
                    url(r"permission/create$",permission_create),
                    url(r"permission/check_value_exists$",check_value_exists),
                    url(r"permission/delete$",permission_delete),
                    url(r"permission/(\d{1,6})/update_name",update_name),
                    url(r"permission/(\d{1,6})/update_desc",update_desc),
                 ]