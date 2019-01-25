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
from doraemon.interface.pagefactory.env_portal_pageworker import ENVPortalPageWorker

@login_required
def all(request):
    ''' index page'''
    page_worker=ENVPortalPageWorker(request)
    return page_worker.get_env_fullpage(request,"all")



@login_required
def env_filter(request):
    filter=request.POST.get('project_filter',"all")
    