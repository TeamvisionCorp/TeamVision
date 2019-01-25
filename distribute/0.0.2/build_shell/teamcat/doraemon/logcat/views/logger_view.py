#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from business.logcat.logger_service import LoggerService
from django.contrib.auth.decorators import login_required
from doraemon.logcat.pagefactory.logger_pageworker import LoggerPageWorker
from gatesidelib.common.simplelogger import SimpleLogger

        

@login_required
def all(request):
    ''' index page'''
    result=""
    try:
        page_worker=LoggerPageWorker(request)
        result=page_worker.get_logger_fullpage(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def more_business_log(request):
    try:
        page_worker=LoggerPageWorker(request)
        result=page_worker.more_businesslog(request)
    except Exception as ex:
        result="False"
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def remove_logger(request,logger_id):
    result=True
    try:
        LoggerService.delete_logger(int(logger_id))
    except Exception as ex:
        result="False"
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def get_logger_list(request):
    result=True
    try:
        page_worker=LoggerPageWorker(request)
        result=page_worker.get_logger_list_controll()
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)
    


    

    
    
    
    
    
    


    