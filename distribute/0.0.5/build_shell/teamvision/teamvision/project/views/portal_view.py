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
from teamvision.project.pagefactory.project_portal_pageworker import ProjectPortalPageWorker

@login_required
def all(request):
    ''' index page'''
    print(1111)
    page_worker=ProjectPortalPageWorker(request)
    return page_worker.get_project_fullpage(request,"all")



@login_required
def project_filter(request):
    filter=request.POST.get('project_filter',"all")
    