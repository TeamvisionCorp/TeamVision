#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from doraemon.ci.pagefactory.ci_task_pageworker import CITaskPageWorker
from doraemon.ci.models import CITask
from gatesidelib.common.simplelogger import SimpleLogger
from json.encoder import JSONEncoder
from business.ci.ci_task_service import CITaskService
from business.ci.ci_task_history_service import CITaskHistoryService
from business.ci.ci_task_config_service import CITaskConfigService
from doraemon.home.models import FileInfo
from doraemon.settings import WEB_HOST
from gatesidelib.qr_code_helper import QRCodeHelper
from business.common.file_info_service import FileInfoService



@login_required
def create_dialog(request):
    ''' index page'''
    page_worker=CITaskPageWorker(request)
    return HttpResponse(page_worker.get_ci_task_create_dialog(request))

@login_required
def confirm_dialog(request):
    ''' index page'''
    page_worker=CITaskPageWorker(request)
    return HttpResponse(page_worker.get_ci_task_confirm_dialog())


@login_required
def create(request):
    taskid=0
    try:
        ci_task=CITaskService.create_ci_task(request)
        taskid=ci_task.id
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(taskid)


@login_required
def copy(request,task_id):
    result="True"
    try:
        CITaskService.copy_ci_task(request,task_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
        
    return HttpResponse(result)


@login_required
def delete_task(request,task_id):
    result="True"
    try:
        CITaskService.delete_ci_task(request,task_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def clean_task_history(request,task_id):
    result="True"
    try:
        CITaskService.clean_task_history(request,task_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def search_task(request):
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.search_tasks(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def filter_task(request):
    pass

def copy_task(request):
    result=CITaskConfigService.copy_config("586b63f56a3c277a1fb4451f")
    return HttpResponse(result)


def start_task(request,task_id):
    result="Flase"
    try:
        parameter_group_id=request.POST.get('parameter_group_id')
        result=CITaskService.start_ci_task(request,task_id,parameter_group_id,0)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def stop_task(request,task_id):
    result="Flase"
    try:
        result=CITaskService.stop_ci_task(request,task_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)
    

@login_required
def task_config_basic(request,task_id):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.get_ci_task_config_basic(request,task_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def download_package_list(request,history_id):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.get_downlaod_package_list(history_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)


# @login_required
def get_task_list(request):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        task_id=request.POST.get("task_id")
        ci_task=CITask.objects.get(int(task_id))
        sub_nav_action=request.POST.get("sub_nav_action")
        dm_ci_tasks=CITaskService.get_product_ci_tasks(request, ci_task.TaskType, sub_nav_action)
        result=page_worker.get_ci_task_list_controll(request,dm_ci_tasks,True)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def more_dashboard_task_list(request):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.dashboard_more_task_list(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def more_history_list(request,task_id):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.task_more_history_list(request,task_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def more_changelog_list(request,task_id):
    ''' index page'''
    result=""
    try:
        page_worker=CITaskPageWorker(request)
        result=page_worker.task_more_changelog_list(request, task_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def save_task_config(request,task_id):
    ''' index page'''
    message="True"
    try:
        CITaskService.save_task_config(request,task_id) 
    except Exception as ex:
        message=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(message)



@login_required
def get_task_config(request,task_id):
    ''' index page'''
    task_config=CITaskConfigService.get_ci_task_config_by_taskid(task_id)
    json_encoder=JSONEncoder()
    return HttpResponse(json_encoder.encode(str(task_config)))


@login_required
def update_property(request,task_id):
    result=True
    try:
        CITaskService.update_property(request,task_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
        
    return HttpResponse(result)



def mobile_download_page(request):
    user_agent=request.META['HTTP_USER_AGENT']
    host=request.META['HTTP_HOST']
    file_id=request.GET.get('file_id',0)
    history_id=request.GET.get('history_id',0)
    os_name="Android"
    android=True
    if 'MAC' in user_agent.upper():
        FileInfoService.create_package_plist(file_id,history_id)
        FileInfoService.create_package_file(file_id)
        package=WEB_HOST.replace('http','https')+"/static/plist_files/"+str(file_id)+".plist"
        os_name="iPhone"
        android=False
    else:
        package=WEB_HOST+"/ci/history/"+str(file_id)+"/download_package"
    
    page_fileds={'package':package,"os_name":os_name,'android':android}
    return render_to_response('task_history/ci_mobile_package_download.html',page_fileds)


    
@login_required
def qr_code(request):
    try:
        content=request.GET.get('content',"")
        file_id=request.GET.get('file_id',"")
        history_id=request.GET.get('history_id',"")
        code_image=QRCodeHelper.save_qr_code_stream(content+"&file_id="+str(file_id)+"&history_id="+str(history_id))
        response = HttpResponse(code_image, content_type="image/png")
    except Exception as ex:
        SimpleLogger.exception(ex)
    return response
    
    

def download_package(request,file_id):
    try:
        file=FileInfo.objects.get(int(file_id))
        contents=FileInfoService.download_file(file_id)
        def file_iterator(chunk_size=1024*50):
            while True:
                c = contents.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        result=StreamingHttpResponse(file_iterator(), content_type='application/octet-stream')
        display_file_name=str(file.FileName.encode("utf-8")).replace("'","")
        result['Content-Disposition'] = 'attachment;filename="'+display_file_name+'"'
    except  Exception as ex:
        result=HttpResponse(str(ex))
        SimpleLogger.exception(ex)
    return result

    
    
    


    