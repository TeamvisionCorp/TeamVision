#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''
from doraemon.administrate.pagefactory.administrate_pageworker import AdminPageWorker
from doraemon.administrate.viewmodels.admin_left_nav_bar import AdminUserLeftNavBar
from doraemon.administrate.viewmodels.admin_sub_nav_bar import AdminUserSubNavBar
from doraemon.administrate.pagefactory.admin_template_path import AdminUserPath
from doraemon.administrate.viewmodels.vm_admin_user import VM_AdminUser
from business.auth_user.user_service import UserService
from django.contrib.auth.models import User
import random

class AdminUserPageWorker(AdminPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        AdminPageWorker.__init__(self, request)
        self.left_nav_bar_model=AdminUserLeftNavBar
        self.subpage_model=AdminUserSubNavBar
    
    def get_admin_user_page(self,request,sub_nav_action):
        sub_leftnav=self.get_user_sub_navbar(request,sub_nav_action)
        left_nav_bar=self.get_admin_left_bar(request,sub_nav_action)
        admin_user_webpart=self.get_user_list_webpart()
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"admin_user_webpart":admin_user_webpart}
        return self.get_page(pagefileds,AdminUserPath.admin_user_index,request)
    
    def get_admin_user_edit_page(self,request,userid,sub_nav_action):
        sub_leftnav=self.get_user_sub_navbar(request,sub_nav_action)
        left_nav_bar=self.get_admin_left_bar(request,sub_nav_action)
        admin_user_edit_webpart=self.get_user_edit_webpart(userid)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"admin_user_edit_webpart":admin_user_edit_webpart}
        return self.get_page(pagefileds,AdminUserPath.admin_user_index,request)
    
    def get_admin_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,AdminUserPath.admin_user_left_nav,sub_nav_action=sub_nav_action)
    
    def get_user_sub_navbar(self,request,sub_nav_action):
        users_count=len(UserService.all_users())
        return self.get_sub_nav_bar(request, self.subpage_model,AdminUserPath.admin_user_subnav,sub_nav_action=sub_nav_action,users_count=users_count)
    
    def get_user_list_webpart(self):
        users=UserService.all_users()
        user_list_controll=self.get_user_list_controll(users)
        pagefileds={"user_list_controll":user_list_controll,"users":users}
        return self.get_webpart(pagefileds,AdminUserPath.admin_user_list_webpart)
    
    def get_user_edit_webpart(self,userid):
        user=UserService.get_user(userid)
        tmp_user=VM_AdminUser(user,is_create=False)
        user_form=self.get_webpart({"user":tmp_user},AdminUserPath.admin_user_form)
        pagefileds={"user_info":user_form,"user":tmp_user}
        return self.get_webpart(pagefileds,AdminUserPath.admin_user_edit_page)
    
    def get_user_list_controll(self,users):
        vm_users=list()
        for user in users:
            tmp_user=VM_AdminUser(user)
            vm_users.append(tmp_user)
        pagefileds={"users":vm_users}
        return self.get_webpart(pagefileds, AdminUserPath.admin_user_list_control)
    
    def get_user_create_dialog(self,request):
        tmp_user=VM_AdminUser(None,is_create=True)
        user_form=self.get_webpart({"user":tmp_user},AdminUserPath.admin_user_form)
        return self.get_page({"formhtml":user_form},AdminUserPath.admin_user_create_dialog,request)
        
        
        
        
    
  
    