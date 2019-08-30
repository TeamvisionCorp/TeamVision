#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.pagefactory.worker import Worker
from django.template import RequestContext
from django.shortcuts import render_to_response
from teamvision.auth_extend.user.viewmodels.vm_user import VM_User
from business.auth_user.user_service import UserService
from teamvision.auth_extend.user.pagefactory.user_template_path import UserResgistrationPath
import random

class UserResgistrationPageWorker(Worker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        Worker.__init__(self, request)
    
    def user_login_page(self,request,message):
        login_background="url(/static/global/images/login/login"+str(random.randint(1, 10))+".jpg)"
        pagefileds={"login_background":login_background,"request":request,"message":message}
        return self.get_page(pagefileds,UserResgistrationPath.user_login_path,request)    
    