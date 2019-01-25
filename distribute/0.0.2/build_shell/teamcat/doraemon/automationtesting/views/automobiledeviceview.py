#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from business.automationtesting.automobiledeviceservice import AutoMobileDeviceService
from doraemon.automationtesting.viewmodels.vm_automobiledevice import VM_AutoMobileDevice
from django.http import HttpResponse


def index_list(request):
    ''' index page'''
    return render_to_response('automobiledevice/automobiledeviceindexview.html')

def get_list(request):
    ''' get all automobiledevice list'''
    try:
        automobiledevicelist=list()
        result=AutoMobileDeviceService.vm_getall_automobiledevice(request)
        for item in result:
            vm_automobiledevice=VM_AutoMobileDevice(item)
            automobiledevicelist.append(vm_automobiledevice)
    except Exception as ex:
        print(ex)
    return render_to_response('automobiledevice/automobiledevicelistcontroll.html', {'automobiledevicelist': automobiledevicelist})

    
def create_add(request):
    ''' create new automobiledevice'''
    if request.method=="POST":
        message=AutoMobileDeviceService.dm_createautomobiledevice(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('automobiledevice/automobiledeviceformview_test.html')



def update_edit(request):
    ''' edit automobiledevice'''
    if request.method=="POST":
        message=AutoMobileDeviceService.dm_updateautomobiledevice(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('automobiledevice/automobiledeviceformview_edit.html')


def init_automobiledevice_formcontrol(request):
    try:
        result=AutoMobileDeviceService.init_automobiledevice_form_control(request)
    except Exception as ex:
        print(ex)
    return HttpResponse(result)

def get_automobiledevice_page_counts(request):
    
    return HttpResponse(AutoMobileDeviceService.get_automobiledevice_page_counts(request))



def copy_automobiledevice(request):
    return HttpResponse(AutoMobileDeviceService.copy_automobiledevice(request))

def delete_automobiledevice(request):
    return HttpResponse(AutoMobileDeviceService.disable_automobiledevice(request))
    