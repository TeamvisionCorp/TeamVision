#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.resources.project.resource_string import Project as ProjectRes
from doraemon.project.models import Project
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from doraemon.project.pagefactory.project_settings_pageworker import ProjectSettingsPageWorker
from business.project.memeber_service import MemberService

        


@login_required
def add(request,projectid):
    result=True
    try:
        member_ids=request.POST.get("user_ids")
        if member_ids!="null":
            print(eval(member_ids))
            for member_id in eval(member_ids+","):
                MemberService.add_member(int(member_id),projectid,request.user)
    except Exception as ex:
        result=ProjectRes.project_member_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def import_member(request,projectid):
    result=True
    try:
        from_project_id=request.POST.get("from_project")
        from_project_members=MemberService.get_member_users(int(from_project_id))
        current_project_members=MemberService.get_member_users(int(projectid))
        for member in from_project_members:
            if member not in current_project_members:
                MemberService.add_member(int(member.id),projectid,request.user)
    except Exception as ex:
        result=ProjectRes.project_member_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)
    
@login_required
def remove(request,projectid):
    result=True
    try:
        MemberService.remove_member(request,projectid)
    except Exception as ex:
        result=ProjectRes.project_member_remove_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def update_member_role(request,projectid,userid):
    result=True
    try:
        MemberService.update_role(request,projectid,userid)
    except Exception as ex:
        result=ProjectRes.project_member_update_role_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def get_member_list(request,projectid):
    result=False
    try:
        page_worker=ProjectSettingsPageWorker(request)
        result=page_worker.get_project_member_list_controll(projectid,request.user)
    except Exception as ex:
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def get_member_add_dialog(request,projectid):
    result=False
    try:
        page_worker=ProjectSettingsPageWorker(request)
        result=page_worker.get_project_member_add_dialog(request,projectid)
    except Exception as ex:
        SimpleLogger.error(ex)
    return HttpResponse(result)



@login_required
def member_dropdownlist(request,project_id):
    result=""
    project=Project.objects.get(int(project_id))
    if project:
        page_worker=ProjectCommonControllPageWorker(request)
        member_users=MemberService.get_member_users(project_id)
        result=page_worker.get_member_dropdownlist(member_users, project.id,0)
    return HttpResponse(result)


    
    
    
    


    