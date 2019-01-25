#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.decorators import login_required
from teamvision.home.viewmodels.vm_home import VM_Home

from teamvision.home.pagefactory.home_fortesting_pageworker import HomeForTestingPageWorker


        

@login_required
def all(request,sub_nav_action):
    ''' index page'''
    page_worker=HomeForTestingPageWorker(request)
    return page_worker.get_full_page(request,sub_nav_action)
    
    
    


    