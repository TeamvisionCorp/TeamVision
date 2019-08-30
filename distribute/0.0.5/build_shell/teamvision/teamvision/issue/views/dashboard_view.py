#coding=utf-8
#coding=utf-8
'''
Created on 2017年5月22日

@author: ethan
'''



from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from teamvision.interface.pagefactory.env_dashboard_pageworker import ENVDashBoardPageWorker

@login_required
def index(request,env_id):
    ''' index page'''
    page_worker=ENVDashBoardPageWorker(request)
    return page_worker.get_dashboard_index(request,"all")

    