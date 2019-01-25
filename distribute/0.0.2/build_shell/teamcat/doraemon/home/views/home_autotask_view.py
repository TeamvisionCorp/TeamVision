#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.decorators import login_required
from doraemon.home.pagefactory.home_autotask_pageworker import HomeAutoTaskPageWorker


        

@login_required
def index_list(request,sub_nav_action):
    ''' index page'''
    page_worker=HomeAutoTaskPageWorker(request)
    return page_worker.get_autotask_fullpage(request, sub_nav_action)


    
    
    
    


    