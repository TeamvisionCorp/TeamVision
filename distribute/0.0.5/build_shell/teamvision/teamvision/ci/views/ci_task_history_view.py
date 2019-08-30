#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.shortcuts import render_to_response
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.ci.pagefactory.ci_template_path import CITaskPath
from business.ci.ci_task_history_service import CITaskHistoryService
from teamvision.ci.pagefactory.ci_task_pageworker import CITaskPageWorker
from teamvision.home.models import FileInfo


@login_required
def get_build_log(request,file_id):
    contents=CITaskHistoryService.get_big_build_log(request,file_id)
    def file_iterator(chunk_size=1024*2):
        while True:
            try:
                c = contents.read(chunk_size)
                result=c.decode('utf-8')
                result=CITaskHistoryService.format_build_log(result)
                if c:
                    yield result
                else:
                    break
            except Exception as ex:
                SimpleLogger.exception(ex)
                continue
    def file_iterator2(chunk_size=1024*2):
        while True:
            try:
                c = contents.read(chunk_size)
                result=c.decode('utf-8')
                result=CITaskHistoryService.format_build_log(result)
                result=result.replace("</br>",'\r\n')
                if c:
                    yield result
                else:
                    break
            except Exception as ex:
                SimpleLogger.exception(ex)
                continue
    if contents.length>1024*1024*10:
        file=FileInfo.objects.get(int(file_id))
        result=StreamingHttpResponse(file_iterator2(), content_type='application/octet-stream')
        display_file_name=str(file.FileName.encode("utf-8")).replace("'","").replace("b'",'')
        result['Content-Disposition'] = 'attachment;filename="'+display_file_name+'"'
    else:
        result=StreamingHttpResponse(file_iterator(),content_type='text/html')
    return result


@login_required
def changelog_detail(request,history_id,change_version):
    page_worker=CITaskPageWorker(request)
    result=page_worker.task_changelog_detail(history_id, change_version)
    return HttpResponse(result)

    