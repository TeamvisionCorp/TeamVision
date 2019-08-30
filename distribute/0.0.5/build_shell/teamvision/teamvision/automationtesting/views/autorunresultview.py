#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from business.automationtesting.autorunresultservice import AutoRunResultService
from teamvision.automationtesting.viewmodels.vm_autorunresult import VM_AutoRunResult
from django.http import HttpResponse


def index_list(request):
    ''' index page'''
    return render_to_response('autorunresult/autorunresultindexview.html')

def get_list(request):
    ''' get all autorunresult list'''
    try:
        autorunresultlist=list()
        result=AutoRunResultService.vm_getall_autorunresult(request)
        for item in result:
            vm_autorunresult=VM_AutoRunResult(item)
            autorunresultlist.append(vm_autorunresult)
    except Exception as ex:
        print(ex)
    return render_to_response('autorunresult/autorunresultlistcontroll.html', {'autorunresultlist': autorunresultlist})

    
def create_add(request):
    ''' create new autorunresult'''
    if request.method=="POST":
        message=AutoRunResultService.dm_createautorunresult(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autorunresult/autorunresultformview_test.html')



def update_edit(request):
    ''' edit autorunresult'''
    if request.method=="POST":
        message=AutoRunResultService.dm_updateautorunresult(request)
        return HttpResponse(message)
    else:
        pass
    return render_to_response('autorunresult/autorunresultformview_edit.html')


def init_autorunresult_formcontrol(request):
    try:
        result=AutoRunResultService.init_autorunresult_form_control(request)
    except Exception as ex:
        print(ex)
    return HttpResponse(result)

def get_autorunresult_page_counts(request):
    
    return HttpResponse(AutoRunResultService.get_autorunresult_page_counts(request))



def copy_autorunresult(request):
    return HttpResponse(AutoRunResultService.copy_autorunresult(request))

def delete_autorunresult(request):
    return HttpResponse(AutoRunResultService.disable_autorunresult(request))
    