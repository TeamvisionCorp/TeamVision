#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from teamvision.administrate.views.admin_user_view import user,user_create_dialog,user_create,user_edit_post,update_group,reset_password
from teamvision.administrate.views.admin_user_view import check_value_exists,user_list,user_delete,user_edit_get

admin_user_router=[
                    url(r"user/(all)$",user),
                    url(r"user/create_dialog$",user_create_dialog),
                    url(r"user/create$",user_create),
                    url(r"user/check_value_exists$",check_value_exists),
                    url(r"user/user_list$",user_list),
                    url(r"user/delete$",user_delete),
                    url(r"user/(\d{1,6})/edit$",user_edit_get),
                    url(r"user/(\d{1,6})/edit_post$",user_edit_post),
                    url(r"user/(\d{1,6})/update_group",update_group),
                    url(r"user/(\d{1,6})/reset_password",reset_password),
                 ]