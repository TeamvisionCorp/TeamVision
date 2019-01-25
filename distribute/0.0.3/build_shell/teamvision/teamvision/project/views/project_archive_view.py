#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.project.pagefactory.project_archive_pageworker import ProjectArchivePageWorker
from business.common.file_info_service import FileInfoService
from teamvision.api.ci.mongo_models import ReleaseArchiveMongoFile
from teamvision.home.models import FileInfo

        


@login_required
def index(request,projectid,version_id):
    result=True
    try:
        page_worker=ProjectArchivePageWorker(request)
        result=page_worker.get_index_page(request, projectid,"all")
    except Exception as ex:
        result=str(ex)
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def archive_file(request,projectid,version_id):
    result=True
    try:
        page_worker=ProjectArchivePageWorker(request)
        result=page_worker.get_archive_item(projectid,version_id)
    except Exception as ex:
        result=str(ex)
        SimpleLogger.error(ex)
    return HttpResponse(result)


def download_package(request,file_id):
    try:
        file=FileInfo.objects.get(int(file_id))
        contents=FileInfoService.download_file(file_id,mongo_model=ReleaseArchiveMongoFile)
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


    
    
    
    


    