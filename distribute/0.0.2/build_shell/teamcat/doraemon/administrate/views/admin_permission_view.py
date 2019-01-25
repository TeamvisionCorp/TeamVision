#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from doraemon.administrate.pagefactory.admin_permission_pageworker import AdminPermissionPageWorker
from business.auth_user.permission_service import PermissionService
from gatesidelib.common.simplelogger import SimpleLogger


@login_required
def permission(request,sub_nav_action):
    page_worker=AdminPermissionPageWorker(request)
    return page_worker.get_admin_permission_page(request, sub_nav_action)


@login_required
def permission_create_dialog(request):
    page_worker=AdminPermissionPageWorker(request)
    return page_worker.get_permission_create_dialog(request)
        
@login_required
def permission_create(request):
    result=True
    try:
        PermissionService.create_permission(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@login_required
def check_value_exists(request):
    result=False
    filed_name=request.POST.get("filed","")
    if filed_name=="codename":
        result=PermissionService.check_codename_exists(request)
    return HttpResponse(result)

@login_required
def permission_list(request):
    page_worker=AdminPermissionPageWorker(request)
    permission_list=page_worker.get_permission_list_controll(PermissionService.all_permissions())
    return HttpResponse(permission_list)

@login_required
def permission_delete(request):
    result=True
    try:
        PermissionService.delete_permission(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)





@login_required
def update_name(request,permissionid):
    result=True
    try:
        PermissionService.update_permission_name(request, permissionid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@login_required
def update_desc(request,permissionid):
    result=True
    try:
        PermissionService.update_permission_desc(request, permissionid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

    


    
        


    

   

    
    
        