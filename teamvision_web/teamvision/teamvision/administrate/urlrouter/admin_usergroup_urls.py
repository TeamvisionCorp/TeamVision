# #coding=utf-8
# # coding=utf-8
# '''
# Created on 2014-1-5
# 
# @author: zhangtiande
# '''
# from django.conf.urls import url
# from doraemon.administrate.views.admin_user_group_view import user_group,group_create,check_value_exists,group_delete,usergroup_list,usergroup_edit_get,group_permission_list,update_description,update_group_permission
# 
# admin_usergroup_router=[
#                     url(r"usergroup/(all)$",user_group),
#                     url(r"usergroup/create$",group_create),
#                     url(r"usergroup/check_value_exists$",check_value_exists),
#                     url(r"usergroup/usergroup_list$",usergroup_list),
#                     url(r"usergroup/(\d{1,6})/delete$",group_delete),
#                     url(r"usergroup/(\d{1,6})/edit_get$",usergroup_edit_get),
#                     url(r"usergroup/(\d{1,6})/update_permission$",update_group_permission),
#                     url(r"usergroup/(\d{1,6})/group_permission_list$",group_permission_list),
#                     url(r"usergroup/(\d{1,6})/update_description",update_description),
#                  ]