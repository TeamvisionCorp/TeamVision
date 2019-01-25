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
from doraemon.home.pagefactory.home_project_pageworker import HomeProjectPageWorker

        

@login_required
def all(request,sub_nav_action):
    ''' index page'''
    page_worker=HomeProjectPageWorker(request)
    return page_worker.get_project_fullpage(request,sub_nav_action)
    
    
    
    
    
    


    