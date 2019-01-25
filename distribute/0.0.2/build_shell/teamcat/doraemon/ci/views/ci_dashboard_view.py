#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.ci.pagefactory.ci_dashboard_pageworker import CIDashBoardPageWorker
from business.ci.ci_task_history_service import CITaskHistoryService
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from business.common.redis_service import RedisService



@login_required
def index_list(request):
    ''' index page'''
    result=""
    try:
        page_worker=CIDashBoardPageWorker(request)
        result=page_worker.get_dashboard_fullpage(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return result

@login_required
def get_build_log_dialog(request):
    ''' index page'''
    result=""
    try:
        page_worker=CIDashBoardPageWorker(request)
        result=page_worker.ci_build_log_dialog(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

def pre_build_log(request):
    ''' index page'''
    result=""
    try:
        page_worker=CIDashBoardPageWorker(request)
        tq_id=request.POST.get('tq_id')
        result=page_worker.get_build_log_content(tq_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

def add_message(request):
    result="OK"
    try:
        message=request.POST.get("msg",'')
        tq_id=request.POST.get("tq_id")
        message_intime=message
        RedisService.append_value("ci_build_log"+tq_id,message_intime,7200)
        welcome = RedisMessage(message_intime)  # create a welcome message to be sent to everybody
        RedisPublisher(facility=tq_id, broadcast=True).publish_message(welcome)
    except Exception as ex:
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@login_required
def get_agent_list(request):
    result=""
    try:
        page_worker=CIDashBoardPageWorker(request)
        result=page_worker.get_dashboard_agent_list_controll(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def get_task_queue_list(request):
    result=""
    try:
        page_worker=CIDashBoardPageWorker(request)
        result=page_worker.get_dashboard_taskqueue_listcontroll(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

    
    
    
    


    