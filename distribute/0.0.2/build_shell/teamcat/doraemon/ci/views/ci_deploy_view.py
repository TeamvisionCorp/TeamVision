#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from doraemon.ci.pagefactory.ci_deploy_pageworker import CIDeployPageWorker
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_service import CITaskService
from gatesidelib.common.simplelogger import SimpleLogger



@login_required
def index_list(request,sub_nav_action):
    ''' index page'''
    page_worker=CIDeployPageWorker(request)
    return page_worker.get_deploy_fullpage(request,sub_nav_action)

@login_required
def config_task(request,task_id,task_property):
    ''' index page'''
    page_worker=CIDeployPageWorker(request)
    return page_worker.get_deploy_task_config_page(request,task_id,task_property)


@login_required
def task_history(request,task_id,task_property):
    ''' index page'''
    page_worker=CIDeployPageWorker(request)
    return page_worker.get_deploy_history_fullpage(request,task_id,task_property)

@login_required
def task_parameter(request,task_id,task_property):
    ''' index page'''
    page_worker=CIDeployPageWorker(request)
    return page_worker.get_deploy_parameter_fullpage(request,task_id,task_property)

@login_required
def build_with_parameter_page(request,task_id,task_property):
    ''' index page'''
    try:
        page_worker=CIDeployPageWorker(request)
        if CITaskParameterService.has_parameters(task_id):
            return page_worker.build_with_parameter_fullpage(request,task_id,task_property)
        else:
            CITaskService.start_ci_task(request,task_id,0,0)
    except Exception as ex:
        SimpleLogger.exception(ex)
    return redirect('/ci/dashboard',request)


@login_required
def task_changelog(request,task_id,task_property):
    ''' index page'''
    page_worker=CIDeployPageWorker(request)
    return page_worker.get_deploy_changelog_fullpage(request,task_id,task_property)
    
    
    
    


    