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
from teamvision.home.pagefactory.home_device_pageworker import HomeDevicePageWorker
from business.administrate.device_service import DeviceService
from gatesidelib.common.simplelogger import SimpleLogger

        

@login_required
def all(request):
    ''' index page'''
    page_worker=HomeDevicePageWorker(request)
    return page_worker.get_device_fullpage(request)


def device_filter(request):
    ''' index page'''
    try:
        page_worker=HomeDevicePageWorker(request)
        web_part_html=page_worker.get_device_list_controll(request)
        print(web_part_html)
    except Exception as ex:
        print(ex)
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
    

    
    
    
    
    
    


    