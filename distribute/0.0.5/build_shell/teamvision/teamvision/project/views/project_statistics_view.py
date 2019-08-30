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
from teamvision.project.pagefactory.project_statistics_pageworker import ProjectStatisticsPageWorker
from gatesidelib.common.simplelogger import SimpleLogger



@login_required
def index(request,projectid,statistics_type):
    ''' index page'''
    page_worker=ProjectStatisticsPageWorker(request)
    return  HttpResponse(page_worker.get_index_page(request, projectid))

@login_required
def issue_count_bystatus(request,projectid,version_id):
    ''' issue summary chart'''
    page_worker=ProjectStatisticsPageWorker(request)
    return  HttpResponse(page_worker.get_statistics_status_summary(projectid,version_id))

    
    


    