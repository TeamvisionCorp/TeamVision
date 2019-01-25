#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.project.pagefactory.project_issue_pageworker import ProjectIssuePageWorker
from business.project.issue_service import IssueService
from business.common.redis_service import RedisService
from teamvision.project.models import ProjectIssue
import time
from io import BytesIO
from business.common.file_info_service import FileInfoService
from teamvision.home.models import FileInfo
from teamvision.project.mongo_models import IssueMongoFile

        


@login_required
def index(request,projectid,issue_id):
    result=True
    try:
        page_worker=ProjectIssuePageWorker(request)
        result=page_worker.get_index_page(request, projectid,issue_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def get_create_dialog(request):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    projectId=request.POST.get('project_id',0)
    return HttpResponse(page_worker.get_issue_create_dialog(request,projectId))

@login_required
def get_upload_dialog(request,issue_id):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    return HttpResponse(page_worker.get_issue_upload_dialog(request,issue_id))


@login_required
def get_issue_operation_dialog(request,issue_id,operation_type):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    return HttpResponse(page_worker.get_issue_operation_dialog(request,issue_id,operation_type))

@login_required
def update_issue_operation_result(request,issue_id,operation_type):
    ''' index page'''
    message="True"
    try:
        solution=request.POST.get("solution")
        comments=request.POST.get("comments")
        IssueService.update_issue_operation_result(issue_id,operation_type,solution,comments,request.user.id)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)



@login_required
def get_issue_filter_save_dialog(request,project_id,query_id):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    return HttpResponse(page_worker.get_issue_filter_save_dialog(request,query_id))



@login_required
def get_issue_detail(request,issue_id):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    return HttpResponse(page_worker.get_issue_detail(int(issue_id)))

@login_required
def get_issue_list(request,project_id):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    user_role=request.POST.get('user_role',"0")
    result=""
    if str(user_role)!="0":
        result=page_worker.get_my_issue_item(request.user.id,user_role)
    else:
        result=page_worker.get_issue_item(int(project_id),request.user.id)
    return HttpResponse(result)

@login_required
def get_issue_more(request,project_id,page_size):
    ''' index page'''
    page_worker=ProjectIssuePageWorker(request)
    page_index=int(page_size)/10
    user_role=request.POST.get('user_role',"0")
    result=""
    if str(user_role)!="0":
        result=page_worker.get_my_issue_more(request.user.id, page_index,user_role)
    else:
        result=page_worker.get_issue_more(int(project_id),request.user.id,page_index)   
    return HttpResponse(result)


@login_required
def create_issue(request):
    message="True"
    try:
        IssueService.create_issue(request)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def create_issue_filter(request,project_id,filter_id):
    message="0"
    try:
        filter_name=request.POST.get('filter_name')
        message=IssueService.create_issue_filter(project_id,filter_id,filter_name,request.user.id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(message)

@login_required
def get_issue_filter_list(request):
    result=""
    try:
        page_worker=ProjectIssuePageWorker(request)
        result=page_worker.get_issue_filter_menu(request.user.id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def get_issue_filter_panel(request,filter_id):
    result=""
    try:
        page_worker=ProjectIssuePageWorker(request)
        result=page_worker.get_issue_filter_body(0,filter_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)


@login_required
def update_issue(request,issue_id):
    message="True"
    try:
        field=request.POST.get('field')
        value=request.POST.get('value')
        new_text=request.POST.get('new_text')
        IssueService.update_issue(issue_id, field, value,new_text,request.user.id)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def add_comment(request,issue_id):
    message="True"
    try:
        comment=request.POST.get('comments')
        issue=ProjectIssue.objects.get(int(issue_id))
        IssueService.create_issue_activity(issue, 0,0,0,comment,request.user.id,1,2)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)


@login_required
def cached_file(request):
    message="0,上传文件超过10M"
    try:
        upload_file=request.FILES['attachment[0]']
        if RedisService.validate_upload_file(upload_file,10*1024*1024,None):
            cached_key=str(request.user.id)+"_"+str(time.time())
            RedisService.set_object(cached_key,upload_file,1800)
            message=cached_key+",null"
    except Exception as ex:
        SimpleLogger.exception(ex)
        message="0,"+str(ex)
    return HttpResponse(message)

@login_required
def remove_cache(request):
    message="True"
    try:
        cache_key=request.POST.get("cache_key")
        RedisService.delete_value(cache_key)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def save_cache(request,issue_id):
    message="True"
    try:
        cache_key=request.POST.get("cache_key")
        tmp_issue=ProjectIssue.objects.get(int(issue_id))
        tmp_issue.Attachments=tmp_issue.Attachments+IssueService.store_cached_file(cache_key)
        tmp_issue.save();
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def cache_issue_filter(request,project_id,filter_id):
    message=True
    try:
        key=str(request.user.id)+"_issue_filter"
        print(request.POST)
        if str(filter_id)=="0":
            values=request.POST.get("values")
            IssueService.cache_issue_filter(key,"Project:"+str(project_id))
            IssueService.cache_issue_filter(key, values)
        else:
            IssueService.update_issue_filter_cache(key, filter_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def cache_issue_search_word(request,project_id):
    message=True
    try:
        word_key=str(request.user.id)+"_issue_searchkeyword"
        filter_key=str(request.user.id)+"_issue_filter"
        value=request.POST.get("search_word")
        IssueService.cache_issue_search_word(word_key,value)
        IssueService.cache_issue_filter(filter_key,"Project:"+str(project_id))
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def clean_issue_filter(request):
    message=True
    try:
        word_key=str(request.user.id)+"_issue_searchkeyword"
        filter_key=str(request.user.id)+"_issue_filter"
        RedisService.delete_value(word_key)
        RedisService.delete_value(filter_key)
    except Exception as ex:
        SimpleLogger.exception(ex)
        message=str(ex)
    return HttpResponse(message)

@login_required
def filter_ui_config(request,filter_id):
    result=""
    try:
        result=IssueService.filter_ui_config(filter_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)

@login_required
def download_file(request,package_file_id):
    result=True
    try:
        file_info=FileInfo.objects.get(int(package_file_id))
        result=FileInfoService.get_file(int(package_file_id),IssueMongoFile)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result,content_type="application/"+file_info.FileSuffixes)

@login_required
def delete_file(request,package_file_id):
    result=True
    try:
        FileInfoService.delete_file(int(package_file_id),IssueMongoFile)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.exception(ex)
    return HttpResponse(result)

def attachment_view(request,issue_id,attachment_id):
    result=""
    try:
        page_worker=ProjectIssuePageWorker(request)
        result=page_worker.get_issue_attachment_viewer(issue_id,attachment_id)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)
    return

def attachment_view_iframe(request,attachment_id):
    result=""
    try:
        page_worker=ProjectIssuePageWorker(request)
        result=page_worker.get_issue_attachment_view_iframe(attachment_id)
        print(result)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)


def export_issue_result(request,project_id):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename='+str(project_id)+'.xls'
    output = BytesIO()
    wb=IssueService.issue_excel_file(project_id,request.user.id)
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response



    
    
    
    


    