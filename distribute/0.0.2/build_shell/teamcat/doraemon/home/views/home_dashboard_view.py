#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from doraemon.home.pagefactory.home_dashboard_pageworker import HomeDashBoardPageWorker



@login_required
def index_list(request):
    ''' index page'''
    page_worker=HomeDashBoardPageWorker(request)
    return page_worker.get_dashboard_fullpage(request)


@login_required
def more_activites(request):
    result="None"
    try:
        page_worker=HomeDashBoardPageWorker(request)
        start_index=request.POST.get("start_index")
        activity_type=request.POST.get("activity_type")
        result=page_worker.get_more_activites(request,int(start_index),activity_type,)
    except Exception as ex:
        result=False
    return HttpResponse(result)
    
    
    
    


    