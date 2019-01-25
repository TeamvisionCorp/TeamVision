#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from doraemon.home.models import FileInfo
from doraemon.project.models import Project
from business.project.fortesting_service import ForTestingService
from business.project.memeber_service import MemberService
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from doraemon.project.pagefactory.project_fortesting_pageworker import ProjectForTestingPageWorker
from doraemon.resources.project.resource_string import Fortesting


@login_required
def all(request,projectid,sub_nav_action):
    ''' index page'''
    page_worker=ProjectForTestingPageWorker(request)
    return page_worker.get_index_page(request, projectid, sub_nav_action)


@login_required
def edit_page(request,projectid,fortesting_id):
    page_worker=ProjectForTestingPageWorker(request)
    return page_worker.get_edit_page(request, projectid, fortesting_id)


@login_required
def edit(request,fortesting_id):
    result=True
    try:
        ForTestingService.edit_fortesting(request, fortesting_id)
    except Exception as ex:
        result=Fortesting.fortesting_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)
    

@login_required
def get_create_dialog(request):
    ''' index page'''
    page_worker=ProjectForTestingPageWorker(request)
    projectId=request.POST.get('project_id',0)
    testApplicationID=request.POST.get("test_application",0)
    return HttpResponse(page_worker.get_fortesting_create_dialog(request,projectId,testApplicationID))


@login_required
def get_confirm_dialog(request):
    ''' index page'''
    page_worker=ProjectForTestingPageWorker(request)
    return HttpResponse(page_worker.get_fortesting_confirm_dialog())

@login_required
def create(request):
    result=True
    try:
        ForTestingService.create_fortesting(request)
    except Exception as ex:
        result=Fortesting.fortesting_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def build(request,fortesting_id):
    result=True
    try:
        ForTestingService.fortesting_build(request,fortesting_id)
    except Exception as ex:
        result=Fortesting.fortesting_build_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def upload_file(request):
    message=0
    try:
        upload_file=request.FILES['attachment[0]']
        message=ForTestingService.attachments_upload_handler(upload_file)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=0
    return HttpResponse(message)


@login_required
def delete_file(request,fortesting_id,file_id):
    message=0
    try:
        ForTestingService.delete_file(fortesting_id,file_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=0
    return HttpResponse(message)

def download(request,package_file_id):
    result=True
    try:
        file_info=FileInfo.objects.get(int(package_file_id))
        result=ForTestingService.download_attachment(int(package_file_id))
    except Exception as ex:
        result=Fortesting.fortesting_build_fail
        SimpleLogger.error(ex)
    return HttpResponse(result,content_type="application/"+file_info.FileSuffixes)

@login_required
def update_status(request,fortesting_id,status):
    result="True"
    try:
        ForTestingService.update_fortesting_status(request.user,fortesting_id,status)
    except Exception as ex:
        result="fail"+Fortesting.fortesting_commit_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)


@login_required
def update_testingdate(request,fortesting_id):
    result="True"
    try:
        start_date=request.POST.get("start_date");
        end_date=request.POST.get("end_date");
        ForTestingService.set_start_end_date(fortesting_id, start_date, end_date)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.error(ex)
    return HttpResponse(result)


@login_required
def get_column_items(request,project_id,item_status):
    ''' index page'''
    page_worker=ProjectForTestingPageWorker(request)
    dm_fortestings=ForTestingService.get_project_fortestings(project_id)
    return HttpResponse(page_worker.get_fortesting_columns_items(dm_fortestings,item_status))


@login_required
def get_module_list(request,project_id):
    result=""
    project=Project.objects.get(int(project_id))
    if project:
        page_worker=ProjectCommonControllPageWorker(request)
        result=page_worker.get_module_dropdown_list(project.id,0)
    print(result)
    return HttpResponse(result)


@login_required
def get_version_list(request,project_id):
    result=""
    default_none=request.POST.get("default_none")
    if str(default_none)=="0":
        default_none=True;
    else:
        default_none=False
    project=Project.objects.get(int(project_id))
    if project:
        page_worker=ProjectCommonControllPageWorker(request)
        result=page_worker.get_version_dropdown_list(project.id,0,default_none)
    return HttpResponse(result)

@login_required
def get_member_list(request,project_id):
    result=""
    project=Project.objects.get(int(project_id))
    if project:
        page_worker=ProjectCommonControllPageWorker(request)
        member_users=MemberService.get_member_users(project_id)
        result=page_worker.get_member_dropdownlist(member_users, project.id)
    return HttpResponse(result)
    
@login_required
def add_tester(request,fortesting_id,tester_id):
    message=True
    try:
        ForTestingService.add_tester(fortesting_id, tester_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def remove_tester(request,fortesting_id,tester_id):
    message=True
    try:
        ForTestingService.remove_tester(fortesting_id, tester_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)


@login_required
def get_fortesting_view_part(request,fortesting_id,is_edit):
    page_worker=ProjectForTestingPageWorker(request)
    if is_edit=="1":
        return HttpResponse(page_worker.get_fortesting_view_part(request, fortesting_id,True))
    else:
        return HttpResponse(page_worker.get_fortesting_view_part(request, fortesting_id,False))
        
@login_required  
def download_attachment(request,file_id):
    try:
        file=FileInfo.objects.get(int(file_id))
        contents=ForTestingService.download_attachment(file.FilePath)
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



    
    


    