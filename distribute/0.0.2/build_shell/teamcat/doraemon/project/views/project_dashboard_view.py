#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext,Context
from django.contrib.auth.decorators import login_required
from doraemon.project.viewmodels.vm_project import VM_Project
from gatesidelib.common.simplelogger import SimpleLogger

from doraemon.project.pagefactory.project_dashboard_pageworker import ProjectDashBoardPageWorker

       

@login_required
def index_list(request,projectid):
    ''' index page'''
#     vm_myplace=VM_Project(request.user)
    pageworker=ProjectDashBoardPageWorker(request);
    left_nav_bar=pageworker.get_dashboard_left_bar(request, projectid)
    activity=pageworker.get_dashboard_activity(request,projectid)
    items=pageworker.get_dashboard_items(request, projectid)
    pagefileds={'left_nav_bar':left_nav_bar,'project_activity':activity,'project_items':items}
    return pageworker.get_full_page_with_header(request, pagefileds, projectid,'dash_board/index.html')


@login_required
def more_activites(request,projectid):
    result="None"
    try:
        page_worker=ProjectDashBoardPageWorker(request)
        start_index=request.POST.get("start_index")
        result=page_worker.get_more_activites(request,projectid,int(start_index))
    except Exception as ex:
        print(ex);
        result=False
    return HttpResponse(result)
    
    
    
    
    


    