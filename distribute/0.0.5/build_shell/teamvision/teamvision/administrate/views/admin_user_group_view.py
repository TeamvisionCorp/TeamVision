# #coding=utf-8
# '''
# Created on 2015-11-30
# 
# @author: zhangtiande
# '''
# 
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.shortcuts import redirect,render_to_response
# # from doraemon.administrate.pagefactory.admin_user_group_pageworker import AdminUserGroupPageWorker
# # from business.auth_user.user_group_service import UserGroupService
# from business.auth_user.permission_service import PermissionService
# from doraemon.decorators.administrate import admin_required
# from gatesidelib.common.simplelogger import SimpleLogger
# 
# 
# @admin_required
# def user_group(request,sub_nav_action):
#     page_worker=AdminUserGroupPageWorker(request)
#     return page_worker.get_admin_usergroup_page(request, sub_nav_action)
#         
# @admin_required
# def group_create(request):
#     result=True
#     try:
#         UserGroupService.create_group(request)
#     except Exception as ex:
#         SimpleLogger.exception(ex)
#         result=str(ex)
#     return HttpResponse(result)
# 
# @admin_required
# def check_value_exists(request):
#     result=False
#     filed_name=request.POST.get("filed","")
#     if filed_name=="group_name":
#         result=UserGroupService.check_groupname_exists(request)
#     return HttpResponse(result)
#  
# @admin_required
# def usergroup_list(request):
#     page_worker=AdminUserGroupPageWorker(request)
#     user_list=page_worker.get_usergroup_list_controll(UserGroupService.all_groups())
#     return HttpResponse(user_list)
#  
# @admin_required
# def group_delete(request,groupid):
#     result=True
#     try:
#         UserGroupService.delete_group(request,groupid)
#     except Exception as ex:
#         print(ex)
#         SimpleLogger.exception(ex)
#         result=str(ex)
#     return HttpResponse(result)
#  
#  
# @admin_required
# def usergroup_edit_get(request,groupid):
#     page_worker=AdminUserGroupPageWorker(request)
#     return page_worker.get_admin_usergroup_edit_page(request,groupid,"all")
#  
# 
# @admin_required
# def update_group_permission(request,groupid):
#     result=True
#     try:
#         UserGroupService.update_group_permission(request,groupid)
#     except Exception as ex:
#         SimpleLogger.exception(ex)
#         result=str(ex)
#     return HttpResponse(result)
# 
# 
# @admin_required
# def group_permission_list(request,groupid):
#     all_custom_permissions=PermissionService.all_custom_permissions()
#     page_worker=AdminUserGroupPageWorker(request)
#     result=page_worker.get_group_permission_controll(all_custom_permissions, groupid)
#     return HttpResponse(result)
# 
# 
# @admin_required
# def update_description(request,groupid):
#     result=True
#     try:
#         UserGroupService.update_group_description(request,groupid)
#     except Exception as ex:
#         SimpleLogger.exception(ex)
#         result=str(ex)
#     return HttpResponse(result)
#         
# 
# 
#     
# 
#    
# 
#     
#     
#         