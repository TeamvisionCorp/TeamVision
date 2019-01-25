#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from doraemon.ci.pagefactory.ci_build_pageworker import CIBuildPageWorker
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_service import CITaskService
from gatesidelib.common.simplelogger import SimpleLogger




@login_required
def index_list(request,sub_nav_action):
    ''' index page'''
    try:
        page_worker=CIBuildPageWorker(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return page_worker.get_build_fullpage(request,sub_nav_action)

@login_required
def build_with_parameter_page(request,task_id,task_property):
    ''' index page'''
    try:
        page_worker=CIBuildPageWorker(request)
        if CITaskParameterService.has_parameters(task_id):
            return page_worker.build_with_parameter_fullpage(request,task_id,task_property)
        else:
            CITaskService.start_ci_task(request,task_id,0,0)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return redirect('/ci/task',request)

@login_required
def config_task(request,takk_id,task_property):
    ''' index page'''
    result=""
    try:
        page_worker=CIBuildPageWorker(request)
        result=page_worker.get_build_task_config_page(request,takk_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def task_history(request,task_id,task_property):
    ''' index page'''
    result=""
    try:
        page_worker=CIBuildPageWorker(request)
        result=page_worker.get_build_history_fullpage(request,task_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def unittest_history(request,task_id,task_property):
    ''' index page'''
    result=""
    try:
        page_worker=CIBuildPageWorker(request)
        result=page_worker.get_unittest_history_fullpage(request,task_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)



@login_required
def task_parameter(request,task_id,task_property):
    ''' index page'''
    result=""
    try:
        page_worker=CIBuildPageWorker(request)
        result=page_worker.get_build_parameter_fullpage(request,task_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def task_changelog(request,task_id,task_property):
    ''' index page'''
    page_worker=CIBuildPageWorker(request)
    return page_worker.get_build_changelog_fullpage(request,task_id,task_property)

@login_required
def history_clean(request,task_id,task_property):
    result=""
    if request.method=="POST":
        pass
#         result=CITaskHistoryService.get_build_log(request,task_id)
    if request.method=="GET":
        page_worker=CIBuildPageWorker(request)
        result=page_worker.build_history_clean_fullpage(request, task_id, task_property)
        
    return HttpResponse(result)