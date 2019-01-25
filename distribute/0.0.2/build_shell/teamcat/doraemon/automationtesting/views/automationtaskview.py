#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from business.automationtesting.automationtaskservice import AutomationTaskService
from doraemon.automationtesting.viewmodels.vm_automationtask import VM_AutomationTask
from django.http import HttpResponse
import socket


def index_list(request):
    ''' index page'''
    return render_to_response('autotask/autotaskindexview.html')

def get_list(request):
    ''' get all autotask list'''
    try:
        autotasklist=list()
        result=AutomationTaskService.vm_getalltasks(request)
        for item in result:
            vm_autotask=VM_AutomationTask(item)
            autotasklist.append(vm_autotask)
    except Exception as ex:
        print(ex)
    return render_to_response('autotask/autolistcontroll.html', {'autotasklist': autotasklist})

def get_mylist(request):
    ''' get all task list'''
    tasklist=AutomationTaskService.vm_getalltasks()
    return render_to_response("autotask/mytasklist.html")

    
def create_add(request):
    ''' create new testtask'''
    if request.method=="POST":
        message=AutomationTaskService.dm_createautotask(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autotask/autotaskformview_test.html')



def update_edit(request):
    ''' edit autotask'''
    if request.method=="POST":
        message=AutomationTaskService.dm_updateautotask(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autotask/autotaskformview_edit.html')

def check_name_exits(request):
    result=AutomationTaskService.check_name_exits(request)
    return HttpResponse(result)

def init_autotask_formcontrol(request):
    try:
        result=AutomationTaskService.init_autotask_form_control(request)
    except Exception as ex:
        print(ex)
    return HttpResponse(result)

def get_autotask_page_counts(request):
    
    return HttpResponse(AutomationTaskService.get_autotask_page_counts(request))

def get_autotask_namelist(request):
    return HttpResponse(AutomationTaskService.get_autotask_namelist())

def copy_autotask(request):
    return HttpResponse(AutomationTaskService.copy_autotask(request))

def delete_autotask(request):
    return HttpResponse(AutomationTaskService.disable_autotask(request))

def start_task(request):
    autotaskid=int(request.POST["autotaskid"])
    AutomationTaskService.start_task(autotaskid,request.META['REMOTE_HOST'],get_remoteip(request))
    return HttpResponse("ID 为: "+str(autotaskid)+"的任务，开始命令，已经发出。请耐心等待。")

def stop_task(request):
    autotaskid=int(request.POST["autotaskid"])
    AutomationTaskService.stop_task(autotaskid,request.META['REMOTE_HOST'],get_remoteip(request))   
    return HttpResponse("ID 为: "+str(autotaskid)+"的任务，停止命令，已经发出。请耐心等待。")

def get_remoteip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']
    return ip
    
    