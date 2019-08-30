#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from teamvision.ci.pagefactory.ci_task_pageworker import CITaskPageWorker
from gatesidelib.common.simplelogger import SimpleLogger
from business.ci.ci_task_parameter_service import CITaskParameterService




@login_required
def edit(request):
    ''' 
       show task parameter edit webpart
    '''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        parameter_id=request.POST.get("parameter_id")
        result=page_worker.get_ci_task_parameter_edit(parameter_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def create(request,task_id):
    '''create a new parameter group after press enter'''
    result=True
    try:
        CITaskParameterService.create_task_parameter(request,task_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def save(request):
    '''save parameter value for exiting parameter group'''
    result=True
    try:
        print(request.POST)
        CITaskParameterService.save_task_parameter(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def delete(request):
    '''save parameter value for exiting parameter group'''
    result=True
    try:
        CITaskParameterService.delete_task_parameter(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def copy(request):
    '''save parameter value for exiting parameter group'''
    result=True
    try:
        CITaskParameterService.copy_task_parameter(request)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def get_task_parameter_group_list(request,task_id):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.get_ci_task_parameter_list(task_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def task_parameter_keyvalue_controll(request):
    ''' index page'''
    return render_to_response('task_parameter/task_parameter_keyvalue.html')

@login_required
def confirm_dialog(request):
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.task_parameter_confirm_dialog(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)
    
    

    
    
    


    