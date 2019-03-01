#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from teamvision.administrate.pagefactory.admin_user_pageworker import AdminUserPageWorker
from business.auth_user.user_service import UserService
from teamvision.decorators.administrate import admin_required,manager_required
from gatesidelib.common.simplelogger import SimpleLogger


@manager_required
def user(request,sub_nav_action):
    page_worker=AdminUserPageWorker(request)
    return page_worker.get_admin_user_page(request, sub_nav_action)


@manager_required
def user_create_dialog(request):
    page_worker=AdminUserPageWorker(request)
    return page_worker.get_user_create_dialog(request)
        
@manager_required
def user_create(request):
    result=True
    try:
        UserService.create_user(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@manager_required
def check_value_exists(request):
    result=False
    filed_name=request.POST.get("filed","")
    if filed_name=="email":
        result=UserService.check_email_exists(request)
    return HttpResponse(result)

@manager_required
def user_list(request):
    page_worker=AdminUserPageWorker(request)
    user_list=page_worker.get_user_list_controll(UserService.all_users())
    return HttpResponse(user_list)

@manager_required
def user_delete(request):
    result=True
    try:
        UserService.delete_user(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)


@manager_required
def user_edit_get(request,userid):
    page_worker=AdminUserPageWorker(request)
    return page_worker.get_admin_user_edit_page(request,userid,"all")

@manager_required
def user_edit_post(request,userid):
    result=True
    try:
        UserService.edit_user(request,userid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)


@admin_required
def update_group(request,userid):
    result=True
    try:
        UserService.update_user_group(request, userid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@manager_required
def reset_password(request,userid):
    result=True
    try:
        UserService.reset_user_password(request, userid)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

    


    
        


    

   

    
    
        