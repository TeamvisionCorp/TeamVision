#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext,Context 
from django.contrib.auth.decorators import login_required
from doraemon.home.viewmodels.vm_home import VM_Home
from django.template.loader import get_template
from doraemon.project.pagefactory.project_task_pageworker import ProjectTaskPageWorker
from business.project.task_service import TaskService
from doraemon.resources.project.resource_string import Task
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.decorators.project import save_to_session



@login_required
def index_list(request,projectid,sub_nav_action):
    ''' index page'''
    page_worker=ProjectTaskPageWorker(request)
    return page_worker.get_project_task_full_page(request, projectid,0,sub_nav_action)

@login_required
def edit(request,projectid,taskid):
    ''' index page'''
    
    page_worker=ProjectTaskPageWorker(request)
    return page_worker.get_task_edit_page(request, projectid, taskid)

@login_required
def get_create_dialog(request):
    ''' index page'''
    page_worker=ProjectTaskPageWorker(request)
    return HttpResponse(page_worker.get_task_create_dialog(request))

@login_required
def create(request):
    result=True
    try:
        TaskService.create_task(request)
    except Exception as ex:
        result=Task.task_save_fail
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def delete(request,taskid):
    result=True
    try:
        TaskService.delete_task(request,taskid)
    except Exception as ex:
        result=Task.task_delete_fail
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def update_property(request,taskid):
    result=True
    try:
        TaskService.update_property(request,taskid)
    except Exception as ex:
        result=Task.task_update_progress_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def more_tasks(request,projectid,sub_nav_action):
    result="None"
    try:
        page_worker=ProjectTaskPageWorker(request)
        start_index=request.POST.get("start_index")
        owner=request.POST.get("owner",0)
        result=page_worker.get_more_tasks(request,projectid,sub_nav_action,owner,int(start_index))
    except Exception as ex:
        print(ex);
        result=False
    return HttpResponse(result)

@login_required
def owner_tasks(request,projectid,sub_nav_action,owner_id):
    result=""
    try:
        page_worker=ProjectTaskPageWorker(request)
        result=page_worker.get_owner_tasks(request,projectid, sub_nav_action, owner_id)
    except Exception as ex:
        SimpleLogger.exception(ex) 
    return HttpResponse(result)



