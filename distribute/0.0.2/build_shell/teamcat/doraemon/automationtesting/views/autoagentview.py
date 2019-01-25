#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from business.automationtesting.autoagentservice import AutoAgentService
from doraemon.automationtesting.viewmodels.vm_autoagent import VM_AutoAgent
from django.http import HttpResponse
from gatesidelib.common.simplelogger import SimpleLogger


def index_list(request):
    ''' index page'''
    return render_to_response('autoagent/autoagentindexview.html')

def get_list(request):
    ''' get all autoagent list'''
    try:
        autoagentlist=list()
        result=AutoAgentService.vm_getall_auotagent(request)
        for item in result:
            vm_autoagent=VM_AutoAgent(item)
            autoagentlist.append(vm_autoagent)
    except Exception as ex:
        print(ex)
    return render_to_response('autoagent/autoagentlistcontroll.html', {'autoagentlist': autoagentlist})

    
def create_add(request):
    ''' create new autoagent'''
    if request.method=="POST":
        message=AutoAgentService.dm_createautoagent(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autoagent/autoagentformview_test.html')



def update_edit(request):
    ''' edit autoagent'''
    if request.method=="POST":
        message=AutoAgentService.dm_updateautoagent(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autoagent/autoagentformview_edit.html')

def check_name_exits(request):
    result=AutoAgentService.check_name_exits(request.POST["agentname"])
    return HttpResponse(result)

def check_ip_exits(request):
    result=AutoAgentService.check_ip_exits(request.POST["agentip"])
    return HttpResponse(result)

def init_autoagent_formcontrol(request):
    try:
        result=AutoAgentService.init_autoagent_form_control(request)
    except Exception as ex:
        print(ex)
    return HttpResponse(result)

def get_autoagent_page_counts(request):
    
    return HttpResponse(AutoAgentService.get_autoagent_page_counts(request))



def copy_autoagent(request):
    return HttpResponse(AutoAgentService.copy_autoagent(request))

def delete_autoagent(request):
    return HttpResponse(AutoAgentService.disable_autoagent(request))
    