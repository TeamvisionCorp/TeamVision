#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from doraemon.device.pagefactory.user_device_pageworker import UserDevicePageWorker
from business.administrate.device_service import DeviceService
from gatesidelib.common.simplelogger import SimpleLogger

        

@login_required
def all(request):
    ''' index page'''
    page_worker=UserDevicePageWorker(request)
    return page_worker.get_device_fullpage(request)


def device_filter(request):
    ''' index page'''
    try:
        page_worker=UserDevicePageWorker(request)
        web_part_html=page_worker.get_device_list_controll(request)
    except Exception as ex:
        SimpleLogger.error(ex)
    return HttpResponse(web_part_html)

def borrow_device(request):
    result=True
    try:
        DeviceService.borrow_device(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.error(ex)
        result=str(ex)
    return HttpResponse(result)
    

    
    
    
    
    
    


    