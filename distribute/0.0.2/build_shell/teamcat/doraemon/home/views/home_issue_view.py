#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.decorators import login_required
from doraemon.home.viewmodels.vm_home import VM_Home

from doraemon.home.pagefactory.home_issue_pageworker import HomeIssuePageWorker


        

@login_required
def all(request,sub_nav_action):
    ''' index page'''
    page_worker=HomeIssuePageWorker(request)
    return page_worker.get_full_page(request,sub_nav_action)
    
    
    


    