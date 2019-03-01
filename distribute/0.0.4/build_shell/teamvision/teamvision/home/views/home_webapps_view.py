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
from teamvision.home.pagefactory.home_webapps_pageworker import HomeWebappsPageWorker
from business.home.webapp_service import WebappService
from teamvision.resources.home.resource_string import WebApp
from gatesidelib.common.simplelogger import SimpleLogger

        

def all(request,sub_nav_action):
    ''' index page'''
    page_worker=HomeWebappsPageWorker(request)
    return page_worker.get_full_page(request,sub_nav_action)

def get_webapp_page(request):
    webapp_html="<iframe src=\"{PAGEURL}\"  width=\"100%\" height=\"100%\" > </iframe>"
    webapp_html=webapp_html.replace("{PAGEURL}",request.POST.get("url"))
    return HttpResponse(webapp_html)

def create(request):
    result=True
    try:
        print(request.POST)
        WebappService.create_webapp(request)
    except Exception as ex:
        result=WebApp.webapp_save_filed
        SimpleLogger.error(ex)
    return HttpResponse(result)

def delete(request):
    result=True
    try:
        print(request.POST)
        WebappService.remove_webapp(request)
    except Exception as ex:
        result=WebApp.webapp_remove_filed
        SimpleLogger.error(ex)
    return HttpResponse(result)
    
    


    
    
    
    
    
    


    