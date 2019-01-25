#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from teamvision.ci.pagefactory.ci_testing_pageworker import CITestingPageWorker
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_service import CITaskService
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.ci.models import CITaskHistory,CITask
from business.ci.ci_testing_history_service import CITestingHistoryService
from io import BytesIO



@login_required
def index_list(request,sub_nav_action):
    ''' index page'''
    result=""
    try:
        page_worker=CITestingPageWorker(request)
        result=page_worker.testing_fullpage(request, sub_nav_action)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def build_with_parameter_page(request,task_id,task_property):
    ''' index page'''
    try:
        page_worker=CITestingPageWorker(request)
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
        page_worker=CITestingPageWorker(request)
        result=page_worker.testing_task_config_page(request,takk_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def run_result(request,task_id,task_property):
    ''' index page'''
    result=""
    try:
        page_worker=CITestingPageWorker(request)
        result=page_worker.testing_result_fullpage(request,task_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def task_parameter(request,task_id,task_property):
    ''' index page'''
    result=""
    try:
        page_worker=CITestingPageWorker(request)
        result=page_worker.testing_parameter_fullpage(request,task_id,task_property)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def result_analytics(request,history_id):
    ''' index page'''
    result=""
    try:
        page_worker=CITestingPageWorker(request)
        result=page_worker.testing_history_analytics(history_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def result_detail(request,history_id,result_type):
    ''' index page'''
    result=""
    try:
        page_worker=CITestingPageWorker(request)
        result=page_worker.testing_case_result_list(history_id,int(result_type))
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def case_result_stace_track(request,case_result_id):
    return "test"


@login_required
def history_clean(request,task_id,task_property):
    result=""
    if request.method=="POST":
        pass
#         result=CITaskHistoryService.get_build_log(request,task_id)
    if request.method=="GET":
        page_worker=CITestingPageWorker(request)
        result=page_worker.build_history_clean_fullpage(request, task_id, task_property)
        
    return HttpResponse(result)


def export_case_result(request,history_id):
    history=CITaskHistory.objects.get(int(history_id))
    ci_task=CITask.objects.get(history.CITaskID)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response[
        'Content-Disposition'] = 'attachment;filename={0}-{1}-{2}.xls'.format(ci_task.TaskName.encode('utf-8'),str(history.ProjectVersion),str(history.BuildVersion))
    output = BytesIO()
    wb=CITestingHistoryService.case_result_excel_file(int(history_id))
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response