#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from teamvision.home.pagefactory.home_unlogin_pageworker import HomeUnloginPageWorker
from teamvision.project.models import Project
from teamvision.project.viewmodels.vm_project import VM_Project
from json.encoder import JSONEncoder
from teamvision.settings import LOG_CONFIG




def home_page(request):
    try:
        if request.user.is_authenticated:
            return redirect("/home/summary")
        else:
            page_worker=HomeUnloginPageWorker(request)
            return page_worker.get_welcome_page(request)
    except Exception as ex:
        message=str(ex)
    return HttpResponse(message)

def project_summary(request):
    page_worker=HomeUnloginPageWorker(request)
    return page_worker.project_summary_page(request)

def device_summary(request):
    if request.user.is_authenticated:
        return redirect("/home/device/all")
    else:
        page_worker=HomeUnloginPageWorker(request)
        return page_worker.device_summary_page(request)


def projects_json(request):
    result=list()
    projects=Project.objects.all()
    for project in projects:
        vm_project=VM_Project(None,False,project,False)
        temp_dict={}
        temp_dict["Project"]=project.PBTitle
        temp_dict["Platform"]=vm_project.platform_title()
        temp_dict["Creator"]=vm_project.project_lead()
        temp_dict["Product"]=vm_project.product_title()
        result.append(temp_dict)
    json_encoder=JSONEncoder()
    return HttpResponse(json_encoder.encode(result))
    
    
    
    
    
    
    


    