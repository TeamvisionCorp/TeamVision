#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from teamvision.user_center.pagefactory.ucenter_account_pageworker import UCenterAccountPageWorker
from business.ucenter.account_service import AccountService
from teamvision.resources.user_center.resource_string import Account
from business.auth_user.user_service import UserService
from gatesidelib.common.simplelogger import SimpleLogger


@login_required
def basic(request,userid,sub_nav_action):
    page_worker=UCenterAccountPageWorker(request)
    return page_worker.get_account_basic_page(request, userid, sub_nav_action)
    
@login_required
def password(request,userid,sub_nav_action):
    page_worker=UCenterAccountPageWorker(request)
    return page_worker.get_account_password_page(request, userid, sub_nav_action)

@login_required
def change_password(request):
    message=True
    try:
        message=UserService.change_password(request)
        if message=="":
            message=True
    except Exception as ex:
        SimpleLogger.error(ex)
        message=str(ex)
        print(message)
    return HttpResponse(message)


@login_required
def upload_avatar(request,userid):
    account_avatar=""
    try:
        message=AccountService.avatar_upload_handler(request)
        if message=="":
            message=Account.ucenter_upload_avatar_fail
        else:
            account_avatar="/ucenter/account/get_avatar/"+message
            message=""
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=Account.ucenter_upload_avatar_fail
        
    return redirect("/ucenter/"+str(userid)+"/account/avatar?message="+message+"&account_avatar="+account_avatar)
    

@login_required
def avatar(request,userid):
    try:
        page_worker=UCenterAccountPageWorker(request)
        avatar_page=page_worker.get_account_avatar_page(request, userid,"basic")
    except Exception as ex:
        SimpleLogger.error(str(ex))
    return avatar_page

@login_required
def avatar_file(request,mongo_file_id):
    try:
        contents=AccountService.get_avatar_file(request,mongo_file_id)
        result=HttpResponse(contents, content_type='image/jpeg')
    except  Exception as ex:
        SimpleLogger.error(str(ex))
    return result

@login_required
def update_avatar(request):
    message=True
    try:
        AccountService.update_avatar(request)
    except Exception as ex:
        SimpleLogger.error(ex)
        message=str(ex)
        print(message)
    return HttpResponse(message)

@login_required
def update_user_info(request):
    message=True
    try:
        AccountService.update_user_info(request)
    except Exception as ex:
        SimpleLogger.error(ex)
        message=str(ex)
        print(message)
    return HttpResponse(message)



    

   

    
    
        