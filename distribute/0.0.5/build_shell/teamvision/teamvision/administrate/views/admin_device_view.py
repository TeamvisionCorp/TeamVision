#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from teamvision.administrate.pagefactory.admin_device_pageworker import AdminDevicePageWorker
from business.administrate.device_service import DeviceService
from teamvision.decorators.administrate import manager_required
from gatesidelib.common.simplelogger import SimpleLogger


@manager_required
def all(request,sub_nav_action):
    page_worker=AdminDevicePageWorker(request)
    return page_worker.get_admin_device_page(request,sub_nav_action)


@login_required
def borrow_device(request):
    result=True
    try:
        DeviceService.borrow_device(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@manager_required
def lend_device(request):
    result=True
    try:
        DeviceService.lend_device(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@manager_required
def return_device(request):
    result=True
    try:
        DeviceService.return_device(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)


@manager_required
def get_devcie_confirm_dialog(request):
    page_worker=AdminDevicePageWorker(request)

    return HttpResponse(page_worker.get_device_borrow_dialog(request))


@manager_required
def device_create_get(request):
    page_worker=AdminDevicePageWorker(request)
    return page_worker.get_device_create_page(request,0)
        
@manager_required
def device_create_post(request):
    result=True
    try:
        DeviceService.create_device_post(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@manager_required
def device_edit_get(request,device_id):
    page_worker=AdminDevicePageWorker(request)
    return page_worker.get_device_create_page(request,device_id)

@manager_required
def device_edit_post(request):
    result=True
    try:
        DeviceService.edit_device_post(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)


@manager_required
def device_list(request):
    page_worker=AdminDevicePageWorker(request)
    device_list=page_worker.get_device_list_controll(DeviceService.all_devices())
    return HttpResponse(device_list)

@manager_required
def device_delete(request):
    result=True
    try:
        DeviceService.delete_device(request)
    except Exception as ex:
        print(ex)
        SimpleLogger.exception(ex)
        result=str(ex)
    return HttpResponse(result)

@manager_required
def get_version_controll(request):
    page_worker=AdminDevicePageWorker(request)
    device_os=int(request.POST.get("device_os"))
    device_os_version_controll=page_worker.get_device_os_version_controll(None,device_os)
    return HttpResponse(device_os_version_controll)



    
        


    

   

    
    
        