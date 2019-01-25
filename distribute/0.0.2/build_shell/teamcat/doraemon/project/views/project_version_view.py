#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.project.pagefactory.project_version_pageworker import ProjectVersionPageWorker
from business.project.version_service import VersionService
from doraemon.resources.project.resource_string import Version


@login_required
def all(request,projectid):
    ''' index page'''
    page_worker=ProjectVersionPageWorker(request)
    return page_worker.get_full_page(request, projectid)

@login_required
def create(request,projectid):
    result=True
    try:
        VersionService.create_version(request, projectid)
    except Exception as ex:
        result=Version.version_save_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def delete(request,projectid,version_id):
    result=True
    try:
        VersionService.delete_version(request,version_id)
    except Exception as ex:
        result=Version.version_delete_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)


@login_required
def update_version(request,projectid,version_id):
    result=True
    try:
        VersionService.update_version(request,version_id)
    except Exception as ex:
        result=Version.version_update_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)

@login_required
def update_date(request,projectid,version_id):
    result=True
    try:
        VersionService.update_date(request,version_id)
    except Exception as ex:
        result=Version.version_update_fail
        SimpleLogger.error(ex)
    return HttpResponse(result)
    

    
    
    
    
    


    