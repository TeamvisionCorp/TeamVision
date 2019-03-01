#coding=utf-8
# coding=utf-8
'''
Created on 2014-3-18

@author: ETHAN
'''

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.project.models import ProjectOSVersion
from teamvision.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from business.common.redis_service import RedisService



@login_required
def os_version_dropdownlist(request,os):
    page_worker=ProjectCommonControllPageWorker(request)
    result=page_worker.get_os_version_dropdown_list(ProjectOSVersion,int(os),0)
    return HttpResponse(result)

@login_required
def os_version_menu(request,os):
    page_worker=ProjectCommonControllPageWorker(request)
    result=page_worker.get_issue_device_version_dropdown_menu(int(os),0)
    return HttpResponse(result)

