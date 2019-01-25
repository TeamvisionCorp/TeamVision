# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.http import HttpResponse
from doraemon.api.ci.json_factory.ci_factory import CIFactory
from business.ci.ci_task_queue_service import CITQService
from business.ci.ci_task_service import CITaskService
from doraemon.api.response.response_models import SuccessResponse,ErrorResponse
from django.contrib.auth.decorators import login_required
from doraemon.resources.ci.resource_string import ResCIService
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.ci.models import CITaskHistory
from business.ci.ci_task_history_service import CITaskHistoryService


def get_task(request):
    try:
        ci_task=CIFactory.get_task(request)
        result=SuccessResponse("success",ci_task)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=ErrorResponse(str(ex),dict())
    return HttpResponse(result.get_json())

def get_task_queue(request):
    try:
        task_queue=CIFactory.get_task_queue(request)
        result=SuccessResponse("success",task_queue)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=ErrorResponse(str(ex),dict())
    return HttpResponse(result.get_json())

def tq_done(request):
    try:
        tq_id=request.GET.get("tq_id","")
        task_history=CITaskHistory.objects.get_by_tqid(int(tq_id))
        CITaskHistoryService.save_build_log(tq_id)
        CITaskHistoryService.clean_build_history(task_history.id)
        CITQService.update_task_queue_status(request)
        CITaskService.send_task_enqueue_message()
        result=SuccessResponse("success",dict())
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=ErrorResponse(str(ex),dict())
    return HttpResponse(result.get_json())

def upload_package(request):
    message=dict()
    message['msg']="success"
    try:
        message['result']=CITaskService.upload_package(request)
        if message['result']=="":
            message['msg']=ResCIService.ci_package_upload_package_fail
    except Exception as ex:
        message['msg']=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(str(message))

