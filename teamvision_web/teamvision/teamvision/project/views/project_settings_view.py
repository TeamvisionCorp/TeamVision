#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext
from teamvision.project.models import Project
from teamvision.resources.project.resource_string import Version,Module
from django.contrib.auth.decorators import login_required
from teamvision.decorators.project import check_value_eixts
from gatesidelib.common.simplelogger import SimpleLogger
from business.project.version_service import VersionService
from business.project.module_service import ModuleService


from teamvision.project.pagefactory.project_settings_pageworker import ProjectSettingsPageWorker
from business.project.project_service import ProjectService

        

@login_required
def basic(request,projectid,sub_nav_action):
    ''' index page'''
    
    page_worker=ProjectSettingsPageWorker(request)
    return page_worker.get_full_page(request, projectid, sub_nav_action)

@login_required
def member(request,projectid,sub_nav_action):
    ''' index page'''
    page_worker=ProjectSettingsPageWorker(request)
    return page_worker.get_full_page(request, projectid, sub_nav_action)


@login_required
def get_create_dialog(request):
    ''' index page'''
    page_worker=ProjectSettingsPageWorker(request)
    return HttpResponse(page_worker.get_settings_create_dialog(request,None))

@login_required
def create(request):
    result=True
    try:
        print(request.POST)
        ProjectService.create_project(request)
    except Exception as ex:
        result="项目创建失败失败,请联系管理员"
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def edit(request,projectid):
    result=True
    try:
        print(request.POST)
        ProjectService.edit_project(request,projectid)
    except Exception as ex:
        result="保存失败,请联系管理员"
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def delete(request,projectid):
    result=True
    try:
        ProjectService.delete_project(request,projectid)
    except Exception as ex:
        result="删除失败，请联系管理员！"
        SimpleLogger.error(ex)
    return HttpResponse(result)



@check_value_eixts(Project)
def check_value_exists(request):
    pass

@login_required
def create_version(request,projectid):
    result=True
    try:
        VersionService.create_version(request, projectid)
    except Exception as ex:
        result=Version.version_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def delete_version(request,projectid,version_id):
    result=True
    try:
        VersionService.delete_version(request,version_id)
    except Exception as ex:
        result=Version.version_delete_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)


@login_required
def update_version(request,projectid,version_id):
    result=True
    try:
        VersionService.update_version(request,version_id)
    except Exception as ex:
        result=Version.version_update_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def update_date(request,projectid,version_id):
    result=True
    try:
        VersionService.update_date(request,version_id)
    except Exception as ex:
        result=Version.version_update_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def create_module(request,projectid):
    result=True
    try:
        ModuleService.create_module(request, projectid)
    except Exception as ex:
        result=Module.module_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def delete_module(request,projectid,module_id):
    result=True
    try:
        ModuleService.delete_module(request, module_id)
    except Exception as ex:
        result= Module.module_delete_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)


@login_required
def update_module(request,projectid,module_id):
    result=True
    try:
        field_name=request.POST.get('field_name')
        value=request.POST.get('field_value')
        ModuleService.update_module(module_id, field_name, value,request.user)
    except Exception as ex:
        result=Module.module_update_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)


    


    