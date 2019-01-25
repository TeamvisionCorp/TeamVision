#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from doraemon.administrate.pagefactory.admin_user_pageworker import AdminUserPageWorker
from business.auth_user.user_service import UserService
from doraemon.decorators.administrate import admin_required,manager_required
from gatesidelib.common.simplelogger import SimpleLogger


@manager_required
def project_list(request):
    return redirect('/project/list/all')




    


    
        


    

   

    
    
        