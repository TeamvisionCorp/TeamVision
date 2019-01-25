#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.decorators import login_required
from doraemon.home.viewmodels.vm_home import VM_Home
from django.http import HttpResponse
from doraemon.home.pagefactory.home_task_pageworker import HomeTaskPageWorker
from gatesidelib.common.simplelogger import SimpleLogger


        

@login_required
def all(request,sub_nav_action):
    ''' index page'''
    page_worker=HomeTaskPageWorker(request)
    return page_worker.get_full_page(request,0,sub_nav_action)


@login_required
def more_tasks(request,sub_nav_action):
    result="None"
    try:
        page_worker=HomeTaskPageWorker(request)
        start_index=request.POST.get("start_index")
        owner=request.POST.get("owner",0)
        result=page_worker.get_more_tasks(request,sub_nav_action,owner,int(start_index))
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=False
    return HttpResponse(result)

@login_required
def owner_tasks(request,sub_nav_action,owner_id):
    result=""
    try:
        page_worker=HomeTaskPageWorker(request)
        result=page_worker.get_owner_tasks(request,0, sub_nav_action, owner_id)
    except Exception as ex:
        SimpleLogger.exception(ex) 
    return HttpResponse(result)
    
    
    
    


    