#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from doraemon.ci.pagefactory.ci_settings_pageworker import CISettingsPageWorker
from doraemon.project.models import Tag
from gatesidelib.common.simplelogger import SimpleLogger
from business.ci.ci_credential_service import CICredentialService
from business.ci.ci_deploy_server_service import CIDeployServerService
from business.ci.ci_agent_service import CIAgentService
from business.project.tag_service import TagService


@login_required
def settings_global_variable(request,sub_nav_action):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_global_fullpage(request,sub_nav_action)


@login_required
def settings_agent(request,sub_nav_action):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_agent_fullpage(request, sub_nav_action)

@login_required
def settings_tag(request,sub_nav_action):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_tag_fullpage(request, sub_nav_action) 

@login_required
def settings_server(request,sub_nav_action):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_server_fullpage(request, sub_nav_action,0) 


@login_required
def settings_credentials(request,sub_nav_action):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_credentials_fullpage(request,sub_nav_action,0) 


@login_required
def credential_create(request):
    result=True
    try:
        CICredentialService.create_ci_credential(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)

@login_required
def credential_edit(request):
    result=True
    try:
        CICredentialService.edit_ci_credential(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)


@login_required
def credential_delete(request,credential_id):
    result=True
    try:
        CICredentialService.delete_ci_credential(request,int(credential_id))
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)


@login_required
def credential_edit_page(request,credential_id):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_credentials_fullpage(request,"",credential_id) 
    

@login_required
def server_create(request):
    result=True
    try:
        CIDeployServerService.create_ci_server(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)

@login_required
def server_edit(request):
    result=True
    try:
        CIDeployServerService.edit_ci_server(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)


@login_required
def server_delete(request,server_id):
    result=True
    try:
        CIDeployServerService.delete_ci_server(request,int(server_id))
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)


@login_required
def server_edit_page(request,server_id):
    page_worker=CISettingsPageWorker(request)
    return page_worker.get_ci_settings_server_fullpage(request,"",server_id) 


@login_required
def agent_create_dialog(request,agent_id):
    page_worker=CISettingsPageWorker(request)
    return HttpResponse(page_worker.get_ci_settings_agent_create_dialog(agent_id))

@login_required
def agent_create(request,agent_id):
    result=True
    try:
        if str(agent_id)=="0":
            CIAgentService.create_ci_agent(request)
        else:
            CIAgentService.edit_ci_agent(request,agent_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)

@login_required
def task_tag_create(request,tag_id):
    result=True
    try:
        tag_name=request.POST.get("TagName")
        if not Tag.objects.has_tag(tag_name):
            if str(tag_id)=="0":
                TagService.create_tag(tag_name,4,request.user.id)
            else:
                TagService.edit_tag(tag_name,int(tag_id))
        else:
            raise Exception("标签名称重复，请更换标签名称")
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)  
    return HttpResponse(result)
    
