#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.resources.project.resource_string import Project

from teamvision.project.pagefactory.project_webhook_pageworker import WebHookPageWorker
from business.project.webhook_service import WebHookService



@login_required
def web_hook(request,projectid,sub_nav_action):
    page_worker=WebHookPageWorker(request)
    return page_worker.get_full_page(request, projectid,sub_nav_action)


@login_required
def add(request,projectid):
    result=True
    try:
        WebHookService.add_webhook(request,projectid)
    except Exception as ex:
        result=Project.project_webhook_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)


@login_required
def edit(request,projectid,webhookid):
    if request.method=="GET":
        page_worker=WebHookPageWorker(request)
        return page_worker.get_edit_page(request, projectid,webhookid)
    if request.method=="POST":
        return update(request,projectid,webhookid)
    


def update(request,projectid,webhookid):
    result=""
    try:
        WebHookService.edit_webhook(request,projectid,webhookid)
    except Exception as ex:
        result=Project.project_webhook_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)
    
@login_required
def remove(request,projectid,webhookid):
    result=True
    try:
        WebHookService.remove_webhook(request,webhookid)
    except Exception as ex:
        result=Project.project_webhook_remove_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def set_default(request,projectid,webhookid):
    is_default=request.POST.get("WHIsDefault")
    if is_default=="false":
        return HttpResponse(Project.project_webhook_set_default_fail)
    else:
        WebHookService.set_webhook_default(request,projectid, webhookid)
        return HttpResponse(True)
        

@login_required
def perform(request,webhook_id):
    result=True
    try:
        WebHookService.perform_hook(request,webhook_id)
    except Exception as ex:
        result=Project.project_webhook_perform_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)
    
    
    
    


    