#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from doraemon.administrate.pagefactory.admin_system_role_pageworker import AdminSystemRolePageWorker
from business.auth_user.system_role_service import SystemRoleService
from business.auth_user.permission_service import PermissionService
from doraemon.decorators.administrate import admin_required
from gatesidelib.common.simplelogger import SimpleLogger


@admin_required
def system_role(request,sub_nav_action):
    page_worker=AdminSystemRolePageWorker(request)
    return page_worker.get_admin_system_role_page(request, sub_nav_action)
        
@admin_required
def role_create(request):
    result=True
    try:
        SystemRoleService.create_role(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@admin_required
def check_value_exists(request):
    result=False
    filed_name=request.POST.get("filed","")
    if filed_name=="group_name":
        result=SystemRoleService.check_rolename_exists(request)
    return HttpResponse(result)
 
@admin_required
def userrole_list(request):
    page_worker=AdminSystemRolePageWorker(request)
    user_list=page_worker.get_system_role_list_controll(SystemRoleService.all_roles())
    return HttpResponse(user_list)
 
@admin_required
def role_delete(request,roleid):
    result=True
    try:
        SystemRoleService.delete_role(request,roleid)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)
 
 
@admin_required
def role_edit_get(request,roleid):
    page_worker=AdminSystemRolePageWorker(request)
    return page_worker.get_admin_system_role_edit_page(request,roleid,"all")
 

@admin_required
def update_role_permission(request,roleid):
    result=True
    try:
        SystemRoleService.update_role_permission(request,roleid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)


@admin_required
def role_permission_list(request,roleid):
    all_custom_permissions=PermissionService.all_custom_permissions()
    page_worker=AdminSystemRolePageWorker(request)
    result=page_worker.get_role_permission_controll(all_custom_permissions, roleid)
    return HttpResponse(result)


@admin_required
def update_description(request,roleid):
    result=True
    try:
        SystemRoleService.update_role_description(request,roleid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)
        


    

   

    
    
        