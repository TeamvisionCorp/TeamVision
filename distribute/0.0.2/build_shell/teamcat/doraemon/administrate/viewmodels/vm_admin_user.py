#coding=utf-8
'''
Created on 2015-11-4

@author: zhangtiande
'''
from django.shortcuts import HttpResponse
from doraemon.project.models import Project,Tag
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService

class VM_AdminUser(object):
    '''
    classdocs
    '''
    
    def __init__(self,user,is_create=False):
        self.user=user
        self.is_create=is_create
        self.admin=""
        self.manager=""
        self.default_group=""
        self.set_user_group()
        
    
    def user_active(self):
        result="finished-check fa-check-square"
        if not self.user.is_active:
            result="fa-square-o unfinished-check"
        return result
        
    
    def user_name(self):
        return self.user.email
    
    def user_full_name(self):
        result=self.user.username
        if self.user.last_name and self.user.first_name:
            result=self.user.last_name+self.user.first_name
        return result
    
    def user_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        if self.user.extend_info:
            result=AccountService.get_avatar_url(self.user)
        return result
    
    def user_groups(self):
        return self.user.groups.all()
    
    def form_id(self):
        result="user_edit_form"
        if self.is_create:
            result="user_create_form"
        return result
    
    def set_user_group(self):
        if self.user:
            if self.user.groups.all().filter(id=27):
                self.admin="checked"
            elif self.user.groups.all().filter(id=28):
                self.manager="checked"
            else:
                self.default_group="checked"
            
    
        