#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from teamvision.ci.pagefactory.ci_service_pageworker import CIServicePageWorker
from gatesidelib.common.simplelogger import SimpleLogger
from business.ci.ci_service import CIService
from teamvision.home.models import FileInfo
from teamvision.resources.ci.resource_string import ResCIService



@login_required
def index(request,sub_nav_action):
    result=""
    try:
        page_worker=CIServicePageWorker(request)
        result=page_worker.get_ci_service_fullpage(request,sub_nav_action)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def service_list(request,sub_nav_action):
    result=""
    try:
        page_worker=CIServicePageWorker(request)
        result=page_worker.get_ci_service_list_controll(request,sub_nav_action)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)






@login_required
def create(request):
    result=0
    try:
        ci_service=CIService.create_ci_service(request)
        result=ci_service.id
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
        
    return HttpResponse(result)




@login_required
def copy(request,service_id):
    result=True
    try:
        CIService.copy_ci_service(request.user,service_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def delete(request,service_id):
    result=True
    try:
        CIService.delete_ci_service(request.user,service_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
        
    return HttpResponse(result)

@login_required
def delete_file(request,file_id):
    result=True
    try:
        CIService.delete_service_file(request,file_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
        
    return HttpResponse(result)



@login_required
def config(request,service_id):
    page_worker=CIServicePageWorker(request)
    return page_worker.get_ci_service_config_page(request,service_id)

@login_required
def config_post(request,service_id):
    result=True
    try:
        CIService.edit_ci_service(request, service_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def replace_config_post(request,service_id):
    result=True
    try:
        CIService.save_replace_config(request, service_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)




@login_required
def upload_file(request,service_id):
    try:
        message=CIService.file_upload_handler(request,service_id)
        if message=="":
            message=ResCIService.ci_service_upload_file_fail
        else:
            message=""
    except Exception as ex:
        SimpleLogger.exception(ex)
    return redirect("/ci/service/"+str(service_id)+"/config")


def download_file(request,file_id):
    try:
        file=FileInfo.objects.get(int(file_id))
        contents=CIService.get_service_file(request,file.FilePath)
        result=HttpResponse(contents, content_type='application/octet-stream')
        display_file_name=str(file.FileName.encode("utf-8")).replace("'","").replace('b','')
        result['Content-Disposition'] = 'attachment;filename="'+display_file_name+'"'
    except  Exception as ex:
        result=HttpResponse(str(ex))
        SimpleLogger.exception(ex)
    return result   