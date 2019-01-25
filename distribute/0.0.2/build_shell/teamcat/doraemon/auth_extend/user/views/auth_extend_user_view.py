#coding=utf-8
'''
Created on 2015-11-30

@author: zhangtiande
'''
from doraemon.auth_extend.user.pagefactory.user_registration_pageworker import UserResgistrationPageWorker
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from business.auth_user.user_service import UserService
from gatesidelib.common.simplelogger import SimpleLogger

def login(request):
    try:
        page_worker=UserResgistrationPageWorker(request)
        if request.method=="GET":
            if not request.user.is_authenticated:
                return page_worker.user_login_page(request,"")
            else:
                return redirect('/home/summary')
        else:
            message= UserService.login(request)
            if message=="":
                return redirect(request.GET.get('next','/home/summary'))
            else:
                return page_worker.user_login_page(request,message)
    except Exception as ex:
        SimpleLogger.exception(ex)
        

def logout(request):
    auth_logout(request)
    return redirect("/")
    
    
        