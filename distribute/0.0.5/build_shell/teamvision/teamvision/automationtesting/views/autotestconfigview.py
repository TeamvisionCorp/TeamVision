#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from business.automationtesting.autotestconfigservice import AutoTestConfigService
from teamvision.automationtesting.viewmodels.vm_autotestconfig import VM_AutoTestConfig
from django.http import HttpResponse


def index_list(request):
    ''' index page'''
    return render_to_response('autotestconfig/autotestconfigindexview.html')

def get_list(request):
    ''' get all autotestconfig list'''
    try:
        autotestconfiglist=list()
        result=AutoTestConfigService.vm_get_all_autotestconfig(request)
        for item in result:
            vm_autotestconfig=VM_AutoTestConfig(item)
            autotestconfiglist.append(vm_autotestconfig)
    except Exception as ex:
        print(ex)
    return render_to_response('autotestconfig/autotestconfiglistcontroll.html', {'autotestconfiglist': autotestconfiglist})

    
def create_add(request):
    ''' create new autotestconfig'''
    if request.method=="POST":
        message=AutoTestConfigService.dm_createautotestconfig(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autotestconfig/autotestconfigformview_test.html')



def update_edit(request):
    ''' edit autotestconfig'''
    if request.method=="POST":
        message=AutoTestConfigService.dm_updateautotestconfig(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autotestconfig/autotestconfigformview_edit.html')

def check_name_exits(request):
    result=AutoTestConfigService.check_name_exits(request)
    return HttpResponse(result)

def init_autotestconfig_formcontrol(request):
    try:
        result=AutoTestConfigService.init_autotestconfig_form_control(request)
    except Exception as ex:
        print(ex)
    return HttpResponse(result)

def get_autotestconfig_page_counts(request):
    
    return HttpResponse(AutoTestConfigService.get_autotestconfig_page_counts(request))


def copy_autotestconfig(request):
    return HttpResponse(AutoTestConfigService.copy_autotestconfig(request))

def delete_autotestconfig(request):
    return HttpResponse(AutoTestConfigService.disable_autotestconfig(request))
    