#coding=utf-8
'''
Created on 2015-11-16

@author: zhangtiande
'''

from django.http.request import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from doraemon.auth_extend.user.datamodels.user_group_enum import UserGroupEnum
from business.auth_user.system_role_service import SystemRoleService


def admin_required(request_func):
    def check_auth(*args,**kwargs):
        if isinstance(args[0],HttpRequest):
            request=args[0]
            if not is_authed(request,UserGroupEnum.Group_Admin):
                return redirect("/user/logout")
            else:
                return request_func(*args,**kwargs)
    return check_auth

def manager_required(request_func):
    def check_auth(*args,**kwargs):
        if isinstance(args[0],HttpRequest):
            request=args[0]
            if not is_authed(request,UserGroupEnum.Grouo_Manager):
                return redirect("/user/logout")
            else:
                return request_func(*args,**kwargs)
    return check_auth


def user_required(request_func):
    def check_auth(*args,**kwargs):
        if isinstance(args[0],HttpRequest):
            request=args[0]
            if not is_authed(request,UserGroupEnum.Group_Admin):
                return redirect("/user/logout")
            else:
                return request_func(*args,**kwargs)
    return check_auth


def is_authed(request,auth_group):
    result=False
    if not request.user.is_authenticated:
        return result
    current_group=SystemRoleService.get_role(auth_group)
    for group in request.user.groups.all():
        if group.extend_info.group_priority<=current_group.extend_info.group_priority:
            result=True
            break
    return result
        
                
                
                




                


    